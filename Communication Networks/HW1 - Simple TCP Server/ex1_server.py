#!/usr/bin/python3
"""
ex1_server.py
Simple non-blocking TCP server used in the exercise.

Overview / Usage
- Run: python ex1_server.py users_file [port]
  - users_file: path to a UTF-8 text file with one user per line: "<username><TAB><password>"
  - port: optional TCP port (default 1337)
- Uses IPv4 TCP (stream) sockets for client connections.

Protocol (line-based, each client message is a single line):
1) Login phase (two-step):
   - Server sends: "Welcome! Please send User: <your username>\n"
   - Client sends exactly one line: "User: <username>"
   - Server does not reply, just waits for password line
   - Client sends exactly one line: "Password: <password>"
   - On success: server sends "Hi <username>, good to see you.\n" and moves client to logged_in state.
   - On failure: server sends "Failed to login.\n" and returns client to await_username.

2) After login, server accepts commands (single-line):
   - "parentheses: <text>"  -> checks balanced parentheses; replies with "the parentheses are balanced: yes/no" or "error: invalid input"
   - "lcm: <a> <b>"         -> returns "the lcm is: <value>" or "error: invalid input"
   - "caesar: <text> <shift>" -> returns "the ciphertext is: <text>" or "error: invalid input"
   - "quit"                 -> server closes the connection
   - any other command -> "error: unknown command" then disconnect

Implementation notes
- Uses select.select for non-blocking multiplexing.
- Each connected socket has an entry in clients mapping. client state = one of:
    - 'await_username'  (expect "User: <username>")
    - 'await_password'  (expect "Password: <password>")
    - 'logged_in'       (accept commands)
- The users file is loaded once at startup by load_users(users_file).
- load_users currently expects a tab-separated username/password per non-empty line.
- safe_send and disconnect_client centralize socket cleanup to avoid crashes on broken pipes.

Limitations / assumptions
- Usernames and passwords must not contain whitespace (current parsing is simple).
- Messages are assumed to be delivered one line at a time (server treats each recv() result as a single line).
- Input validation for commands is permissive but returns clear error messages on malformed input.
"""
import socket
import select
import sys
import math

def is_balanced_parentheses(text):
    """
    Check whether text contains only '(' and ')' and whether they are balanced.

    Returns:
    - 2 : input contains invalid characters (only '(' and ')' are allowed)
    - 1 : parentheses are balanced
    - 0 : parentheses are not balanced
    """
    cnt = 0
    if not all(ch in "()" for ch in text):
        return 2
    for ch in text:
        if cnt < 0:
            break
        if ch == '(':
            cnt += 1
        else: # assuming ch == ')' after input validation
            cnt -= 1
    return 1 if cnt == 0 else 0

def calculate_lcm(x, y):
    """
    Return least common multiple of x and y (both ints).
    Uses gcd from math module for correctness and performance.
    """
    return abs(x*y)//math.gcd(x,y)

def caesar_cipher(text, shift):
    """
    Simple Caesar cipher over ASCII letters.
    - Accepts only ASCII letters A–Z / a–z and space characters.
    - Returns the ciphertext as lowercase letters with spaces preserved.
    - Any other character -> invalid input (returns None).
    """
    if not all((('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ch == ' ') for ch in text):
        return None
    ciphertext = []
    for ch in text:
        if ch ==' ':
            ciphertext.append(ch)
        else:
            ciphertext.append(chr((ord(ch.lower()) - ord('a') + shift) % 26 + ord('a')))
    return "".join(ciphertext)

def load_users(users_file):
    """
    Load users from a file.

    Expected format: each non-empty line is "username<TAB>password".
    Returns a dict mapping username -> password.

    On error reading the file, prints an error and returns an empty dict.
    (The server will continue but no user will be able to log in.)
    """
    users = {}
    try:
        with open(users_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    username, password = line.strip().split('\t')
                    users[username] = password
    except Exception as e:
        print(f"Error reading users file: {e}")
    return users

def disconnect_client(sock, sockets, clients):
    """
    Remove socket from tracking structures and close it safely.
    """
    if sock in sockets:
        sockets.remove(sock)
    if sock in clients:
        del clients[sock]
    try:
        sock.close()
    except OSError:
        pass

def safe_send(sock, msg, sockets, clients):
    """
    Send msg to sock; on common socket errors disconnect the client cleanly.
    msg must be bytes.
    """
    try:
        sock.send(msg)
    except (BrokenPipeError, ConnectionResetError, OSError):
        disconnect_client(sock, sockets, clients)


def main():
    """
    Main server entry point:
    - Parse argv
    - Load users
    - Create non-blocking listening socket
    - Enter select loop to handle multiple clients
    """
    # Argument handling
    if len(sys.argv) < 2:
        print("Usage: ./ex1_server.py users_file [port]")
        return
    users_file = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv)>2 else 1337

    # Load users before allowing connections to server
    users = load_users(users_file)

    # Establish server connection (IPv4/TCP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', port))
    server.listen(5)
    server.setblocking(False)

    sockets = [server] 
    clients = {}

    while True:
        read_sockets, _, _ = select.select(sockets, [], [])
        for sock in read_sockets:
            if sock is server: # New connection
                client, addr = server.accept()
                sockets.append(client)
                clients[client] = {'state': 'await_username'}
                safe_send(client, b"Welcome! Please log in.\n", sockets, clients)
                
            else: # Existing connection
                try:
                    data = sock.recv(1024).decode().strip()
                except:
                    data = None

                if not data: # Client disconnected or error reading
                    sockets.remove(sock)
                    del clients[sock]
                    sock.close()
                    continue

                state = clients[sock]['state']

                # State: expecting username line "User: <username>"
                if state == 'await_username':
                    line = data.strip().split(' ')
                    if not line or line[0] != "User:" or len(line) < 2:
                        safe_send(sock, b"Failed to login.\n", sockets, clients)
                        continue
                    clients[sock]['username_attempt'] = line[1]
                    clients[sock]['state'] = 'await_password'
                    continue

                # State: expecting password line "Password: <password>"
                elif state == 'await_password':
                    line = data.strip().split(' ')
                    if not line or line[0] != "Password:" or len(line) < 2:
                        clients[sock].pop('username_attempt', None)
                        clients[sock]['state'] = 'await_username'
                        safe_send(sock, b"Failed to login.\n", sockets, clients)
                        continue
                    username = clients[sock].pop('username_attempt', None)
                    if username is None:
                        clients[sock]['state'] = 'await_username'
                        safe_send(sock, b"Failed to login.\n", sockets, clients)
                        continue
                    password = line[1]
                    if username in users and users[username] == password:
                        clients[sock]['state'] = 'logged_in'
                        safe_send(sock, f"Hi {username}, good to see you.\n".encode(), sockets, clients)
                    else:
                        clients[sock]['state'] = 'await_username'
                        safe_send(sock, b"Failed to login.\n", sockets, clients)
                        continue

                # Logged-in: accept commands documented above
                elif state == 'logged_in':
                    data = data.strip()
                    if data.startswith("parentheses:"):
                        s = data.split(":", 1)[1].strip()
                        if not s:
                            safe_send(sock, b"error: invalid input\n", sockets, clients)
                            continue
                        res_code = is_balanced_parentheses(s)
                        if res_code == 2:
                            safe_send(sock, b"error: invalid input\n", sockets, clients)
                            continue
                        res = "yes" if res_code == 1 else "no"
                        safe_send(sock, f"the parentheses are balanced: {res}\n".encode(), sockets, clients)

                    elif data.startswith("lcm:"):
                        try:
                            _, a, b = data.split()
                            a, b = int(a), int(b)
                            safe_send(sock, f"the lcm is: {calculate_lcm(a,b)}\n".encode(), sockets, clients)
                        except:
                            safe_send(sock, b"error: invalid input\n", sockets, clients)

                    elif data.startswith("caesar:"):
                        try:
                            _, *text_parts, shift = data.split()
                            shift = int(shift)
                            text = " ".join(text_parts)
                            enc = caesar_cipher(text, shift)
                            if enc is not None:
                                safe_send(sock, f"the ciphertext is: {enc}\n".encode(), sockets, clients)
                            else:
                                safe_send(sock, b"error: invalid input\n", sockets, clients)
                        except:
                            safe_send(sock, b"error: invalid input\n", sockets, clients)

                    elif data == "quit":
                        disconnect_client(sock, sockets, clients)

                    else:
                        safe_send(sock, b"error: unknown command\n", sockets, clients)
                        disconnect_client(sock, sockets, clients)


if __name__ == "__main__":
    main()