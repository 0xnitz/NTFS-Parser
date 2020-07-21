from time import time
from sys import argv

from ntfs_exception import FileNotFoundException
from ntfs_parser import NTFSParser

# CR: [design] This should be part of a function. I would also measure time
# only if requested.
start = time()

# CR: [bug] The program crashes every time I run it

# CR: [design] Let's talk about OOP

# CR: [general] Use an 80 character line boundary
# CR: [finish] Remove comments.
# CR: [design] Let's talk about packages
# CR: [conventions] Mark private members and methods using a preceding '_'.
# This helps understand what are the public interfaces of each entity.

# CR: [requirements] What about letting the user choose a drive?


def main():
    # Arg check
    # CR: [implementation] Use argparse for argument parsing. Put the arg
    # parsing outside main. This will allow others to call main and pass in
    # arguments.
    if len(argv) != 2:
        # CR: [finish] Recommending f-strings
        print('This program will search for a file in file system and print it\'s contents!\n'
              'Usage: {0} filename_to_search'.format(argv[0]))
        exit(1)

    filename = argv[1]

    # Creating the parser and locating the MFT
    # CR: [implementation] Suggesting to use logging utilities for all prints
    # that are not strictly required.
    print('[] Searching for file {0}...'.format(filename))
    parser = NTFSParser()

    try:
        # Starting the scan over the MFT
        ret_val = parser.find_file(filename)

        # Success, print the file's contents
        print('[] Found it!\n{0}\'s contents:\n'.format(filename))
        print(ret_val, end='\n\n')
    except FileNotFoundException:
        # Failure, print an error message
        print('[] {0} file not found!'.format(filename), end='\n\n')

    # Print the parser's runtime
    print('[] Parser finished execution, runtime -> {0}s...'.format(time() - start))


if __name__ == "__main__":
    main()
