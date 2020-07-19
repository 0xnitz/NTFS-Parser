import sys
import time
import os
from ntfs_parser import *

start = time.time()


def main():
    #os.system('wmic partition get StartingOffset, Name, Size')

    # Arg check
    if len(sys.argv) != 2:
        print('This program will search for a file in file system and print it\'s contents!\n'
              'Usage: {0} filename_to_search'.format(sys.argv[0]))
        exit(1)

    filename = sys.argv[1]

    # Creating the parser and locating the MFT
    parser = NTFSParser()
    print('[] Searching for file {0}...'.format(filename))

    # Starting the scan over the MFT
    ret_val = parser.find_file(filename)

    if ret_val != FAILURE:
        # Success, print the file's contents
        print('[] Found it!\n{0}\'s contents:\n'.format(filename))
        print(ret_val, end='\n\n')
    else:
        # Failure, print an error message
        print('[] {0} file not found!'.format(filename), end='\n\n')

    # Print the parser's runtime
    print('[] Parser finished execution, runtime -> {0}s...'.format(time.time() - start))


if __name__ == "__main__":
    main()
