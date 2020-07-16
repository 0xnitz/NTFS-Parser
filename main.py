import sys
import time
from ntfs_parser import *
from constants import *

start = time.time()


def main():
    #if len(sys.argv) != 2:
    #    print('This program will search frch'.format(sys.argv[0]))
    #     #    exit(1)or a file in file system and print it\'s contents!\n'
    #          'Usage: {0} filename_to_sea
    #
    #filename = sys.argv[1]

    filename = '$Quota'
    parser = NTFSParser()
    ret_val = parser.find_file(filename)

    if ret_val != FAILURE:
        print('Found it!\nFile\'s Contents:\n')
        print(ret_val.decode(), end='\n\n')
    else:
        print('File not found!', end='\n\n')

    print('Parser finished execution, runtime -> {0}s'.format(time.time() - start))


if __name__ == "__main__":
    main()
