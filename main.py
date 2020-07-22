from ntfs_exception import FileNotFoundException
from ntfs_parser import NTFSParser

from argparse import ArgumentParser
from time import time


def main(args):
    try:
        parser = NTFSParser()
        ret_val = parser.get_file_contents(filename)

        if args['verbose']:
            print(f'[] Found it!\n[] {filename}\'s contents:\n')

        print(ret_val, end='\n\n')
    except FileNotFoundException:
        if args['verbose']:
            print(f'[] {filename} file not found!', end='\n\n')

    if args['time']:
        print(f'[] Parser finished execution, runtime -> {time() - start}s...')


if __name__ == "__main__":
    arg_parser = ArgumentParser(description='This is an NTFS Parser, give it a filename (not a path) '
                                        'and the program will print it\'s contents!')

    arg_parser.add_argument('-f', '--file', help='The filename you want the parser to find', required=True)

    arg_parser.add_argument('-t', '--time', help='Add runtime measurement', required=False, action='store_true')
    arg_parser.add_argument('-v', '--verbose', help='Adding some prints', required=False, action='store_true')

    arguments = vars(arg_parser.parse_args())

    filename = arguments['file']

    if arguments['time']:
        start = time()

    if arguments['verbose']:
        print(f'[] Searching for file {filename}...')

    main(arguments)
