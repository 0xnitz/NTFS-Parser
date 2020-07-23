from ntfs_exception import NTFSException
from ntfs_parser import NTFSParser

from argparse import ArgumentParser
from time import time


def main(args):
    try:
        parser = NTFSParser(disk)
        file_found = parser.get_file_contents(filename)

        if args.verbose:
            print(f'[] Found it!\n[] {filename}\'s contents:')

        print(file_found.get_data())

    except NTFSException as e:
        if args.verbose:
            print(str(e))

    if args.time:
        print(f'[] Parser finished execution, runtime -> {time() - start}s...')


if __name__ == "__main__":
    arg_parser = ArgumentParser(description='This is an NTFS Parser, give it a filename (not a path) '
                                        'and the program will print it\'s contents!')

    arg_parser.add_argument('-f', '--file', help='The filename you want the parser to find', required=True)
    arg_parser.add_argument('-d', '--disk', help='The disk you want to scan', required=True)

    arg_parser.add_argument('-t', '--time', help='Add runtime measurement', required=False, action='store_true')
    arg_parser.add_argument('-v', '--verbose', help='Adding some prints', required=False, action='store_true')

    arguments = arg_parser.parse_args()

    filename = arguments.file
    disk = arguments.disk

    if arguments.time:
        start = time()

    if arguments.verbose:
        print(f'[] Searching for file {filename}...')

    main(arguments)
