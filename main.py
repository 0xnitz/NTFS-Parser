from ntfs_exception import FileNotFoundException, DiskDoesNotExist
from ntfs_parser import NTFSParser

from argparse import ArgumentParser
from time import time


def main(args):
    try:
        parser = NTFSParser(disk)
        ret_val = parser.get_file_contents(filename)

        # CR: [implementation] Use logging library to control debug prints
        if args['verbose']:
            print(f'[] Found it!\n[] {filename}\'s contents:\n')

        print(ret_val, end='\n\n')
    # CR: [implementation] Just catch NTFSException and print its contents
    except FileNotFoundException:
        if args['verbose']:
            print(f'[] {filename} file not found!', end='\n\n')
    except DiskDoesNotExist:
        if args['verbose']:
            print(f'[] ERROR! Disk {disk} does not exist!')

    if args['time']:
        print(f'[] Parser finished execution, runtime -> {time() - start}s...')


if __name__ == "__main__":
    arg_parser = ArgumentParser(description='This is an NTFS Parser, give it a filename (not a path) '
                                        'and the program will print it\'s contents!')

    arg_parser.add_argument('-f', '--file', help='The filename you want the parser to find', required=True)
    arg_parser.add_argument('-d', '--disk', help='The disk you want to scan', required=True)

    arg_parser.add_argument('-t', '--time', help='Add runtime measurement', required=False, action='store_true')
    arg_parser.add_argument('-v', '--verbose', help='Adding some prints', required=False, action='store_true')

    # CR: [implementation] Why use vars()? You coukd simply do
    # arguments = arg_parser.parse_args()
    # And then
    # arguments.file
    arguments = vars(arg_parser.parse_args())

    filename = arguments['file']
    disk = arguments['disk']

    if arguments['time']:
        start = time()

    if arguments['verbose']:
        print(f'[] Searching for file {filename}...')

    main(arguments)
