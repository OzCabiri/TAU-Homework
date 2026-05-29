from infosec.core import assemble


def patch_program_data(program: bytes) -> bytes:
    """
    Implement this function to return the patched program. This program should
    execute lines starting with #!, and print all other lines as-is.
    
    WARNING! THIS FUNCTION MUST WORK EVEN IF THE SOURCE PROGRAM IS PLACED IN A DIFFERENT PATH!
    Use the provided path to the source program, and avoid hard-coding the path in
    the exercise directory!

    Use the `assemble` module to translate assembly to bytes. For help, in the
    command line run:

        ipython3 -c 'from infosec.core import assemble; help(assemble)'

    :param data: The bytes of the source program.
    :return: The bytes of the patched program.
    """
    patch1 = assemble.assemble_file("patch1.asm")
    pos1 = 0x633
    patch2 = assemble.assemble_file("patch2.asm")
    pos2 = 0x5CD
    
    prog = bytearray(program)
    
    for i in range(len(patch1)):
        prog[pos1+i] = patch1[i]

    for i in range(len(patch2)):
        prog[pos2+i] = patch2[i]
        
    return prog

def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    patched = patch_program_data(data)
    with open(path + '.patched', 'wb') as writer:
        writer.write(patched)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <readfile-program>'.format(argv[0]))
        return -1
    path = argv[1]
    patch_program(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
