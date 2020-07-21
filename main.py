from time import time
from sys import argv

from ntfs_exception import FileNotFoundException
from ntfs_parser import NTFSParser

start = time()


def main():
    if len(argv) != 2:
        print('This program will search for a file in file system and print it\'s contents!\n'
              'Usage: {0} filename_to_search'.format(argv[0]))
        exit(1)

    filename = argv[1]

    print('[] Searching for file {0}...'.format(filename))
    parser = NTFSParser()

    try:
        ret_val = parser.find_file(filename)

        print('[] Found it!\n{0}\'s contents:\n'.format(filename))
        print(ret_val, end='\n\n')
    except FileNotFoundException:
        print('[] {0} file not found!'.format(filename), end='\n\n')

    print('[] Parser finished execution, runtime -> {0}s...'.format(time() - start))


if __name__ == "__main__":
    main()
