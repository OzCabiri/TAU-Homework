#!/usr/bin/python3
"""
Simple TCP client for the exercise server.

Usage:
  python ex1_client.py [host] [port]

Behaviour:
- Connects to the specified server (default localhost:1337).
- Prints any received server lines to stdout.
- Reads user input from stdin, sends each non-empty line to the server
  (appending a newline), and stops when the user types "quit" or when the
  connection is closed.
- Handles common connection errors gracefully and always closes the socket.
"""
import socket
import sys
import select

def main():
    """Run the client: parse args, connect, then enter a send/receive loop."""
    # Argument handling: optional host and port
    host = sys.argv[1] if len(sys.argv)>1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv)>2 else 1337

    # Create TCP socket and connect to server
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
    except Exception as e:
        print(f"Failed to connect to {host}:{port} — {e}")
        return

    # Main communication loop
    try:
        while True:
            rlist, _, _ = select.select([client, sys.stdin], [], [])

            if client in rlist:
                data = client.recv(1024)
                if not data:
                    # server closed
                    break
                # print server output as-is
                print(data.decode(), end='')

            if sys.stdin in rlist:
                line = sys.stdin.readline()
                if line == '':
                    # EOF on stdin
                    break
                msg = line.rstrip('\n')
                if not msg.strip():
                    continue
                try:
                    client.send((msg + '\n').encode())
                except (BrokenPipeError, ConnectionResetError, OSError) as e:
                    print(f"Connection Error: {e}")
                    break
                if msg.strip() == "quit":
                    break
    
    finally:
        client.close()

if __name__ == "__main__":
    main()