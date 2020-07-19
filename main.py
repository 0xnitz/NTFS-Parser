import sys
import time
from ntfs_parser import *

start = time.time()


def main():
    #if len(sys.argv) != 2:
    #    print('This program will search frch'.format(sys.argv[0]))
    #     #    exit(1)or a file in file system and print it\'s contents!\n'
    #          'Usage: {0} filename_to_sea
    #
    #filename = sys.argv[1]

    filename = 'ClassPublic16.svgg'

    parser = NTFSParser()
    print('[] Searching for file {0}...'.format(filename))
    ret_val = parser.find_file(filename)

    if ret_val != FAILURE:
        print('[] Found it!\n{0}\'s contents:\n'.format(filename))
        print(ret_val, end='\n\n')
    else:
        print('[] {0} file not found!'.format(filename), end='\n\n')

    print('[] Parser finished execution, runtime -> {0}s...'.format(time.time() - start))


if __name__ == "__main__":
    main()
