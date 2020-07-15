from parser import *
import sys

def main():
    #if len(sys.argv) != 2:
    #    print('This program will search for a file in file system and print it\'s contents!\n'
    #          'Usage: {0} filename_to_search'.format(sys.argv[0]))
    #    exit(1)
    #
    #filename = sys.argv[1]
    filename = '$MFT'
    parser = Parser()
    parser.find_file(filename)


if __name__ == "__main__":
    main()
