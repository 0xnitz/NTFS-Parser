from attribute_parser import *
from constants import *


class MFTEntry:
    """
    This class represents an MFTEntry.
    """

    def __init__(self, entry):
        self.entry = entry
        self.attribute_parser = AttributeParser()

    def read_resident_data(self):
        """
        Read the data attribute using the MFTParser class
        :return: data attribute contents
        """

        # Cut the $DATA attribute from the entry
        data_attribute = self.attribute_parser.get_attribute(DATA_TYPE, self)

        # If the $DATA attribute is resident, parse and print it's data
        return self.attribute_parser.parse_data(data_attribute)

    def __eq__(self, filename):
        """
        This function will compare between a filename and the MFT Entry's $FILE_NAME attribute
        :param filename: filename to compare to the mft entry (string)
        :return: file's name is equal to filename
        """

        # Checking if the entry is a valid MFT entry
        if not self.is_valid():
            return False

        # Cutting the $FILE_NAME attribute from the entry
        filename_attribute = self.attribute_parser.get_attribute(FILE_NAME_TYPE, self)

        # Entry is not allocated, doesn't have the $FILE_NAME attribute or is a directory return False
        if filename_attribute == UNALLOCATED_ENTRY or\
                filename_attribute == NO_SUCH_ATTRIBUTE or\
                filename_attribute == DIRECTORY:
            return False

        # Extracting the filename text from the attribute, if an exception is thrown ignore it and return False
        try:
            # Extracting the filename from the mft entry
            extracted_filename = self.attribute_parser.parse_filename(filename_attribute).decode()

            # Removing the extra null bytes between each char
            extracted_filename = ''.join(extracted_filename.split('\x00'))
            print(extracted_filename)
        except:
            return False

        # Checking to see if we found the file
        return extracted_filename == filename

    def is_valid(self):
        """
        This function validates an MFT entry.
        *The entry has the FILE signature
        *The entry has a FILE_NAME attribute
        :return: True/False is the entry valid for parsing
        """

        # Checking if the entry has the signature and a $FILE_NAME attribute
        return b'FILE' == self.entry[:0x4] and b'\x30\x00\x00\x00' in self.entry

