from argparse import ArgumentParser
from time import time

from ntfs_exception import FileNotFoundException
from ntfs_parser import NTFSParser


def main(args):
    timer, verbose = False, False

    filename = args['file']

    if args['time'] is not None:
        timer = True
        start = time()

    if args['verbose'] is not None:
        verbose = True
        print(f'[] Searching for file {filename}...')

    try:
        ntfs_parser = NTFSParser()
        ret_val = ntfs_parser.find_file(filename)

        if verbose:
            print(f'[] Found it!\n{filename}\'s contents:\n')

        print(ret_val, end='\n\n')
    except FileNotFoundException:
        if verbose:
            print('[] %s file not found!' % filename, end='\n\n')

    if timer:
        print(f'[] Parser finished execution, runtime -> {time() - start}s...')


if __name__ == "__main__":
    parser = ArgumentParser(description='This is an NTFS Parser, give it a filename (not a path) '
                                        'and the program will print it\'s contents!')

    parser.add_argument('-f', '--file', help='The filename you want the parser to find', required=True)
    parser.add_argument('-d', '--disk', help='The disk you want the parser to search in.'
                                             ' Example: --disk=c', required=True)

    parser.add_argument('-t', '--time', help='Add runtime measurement', required=False)
    parser.add_argument('-v', '--verbose', help='Adding some prints', required=False)

    arguments = vars(parser.parse_args())
    main(arguments)
