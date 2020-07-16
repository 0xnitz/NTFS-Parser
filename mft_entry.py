from attribute_parser import *
from constants import *


class MFTEntry:
    def __init__(self, entry):
        self.entry = entry
        self.mft_parser = MFTParser()

    def read_data(self):
        """
        Read the data attribute using the MFTParser class
        :return: data attribute contents
        """

        data_attribute = self.mft_parser.get_attribute(DATA_TYPE, self)

        if data_attribute == NO_SUCH_ATTRIBUTE:
            return b'$DATA doesn\'t exist!'

        if self.mft_parser.is_resident(data_attribute):
            return self.mft_parser.parse_data(data_attribute)

        return b'This $DATA is non-resident!'

    def __eq__(self, filename):
        """
        This function will compare between a filename and the MFT Entry's $FILE_NAME attribute
        :param filename: filename to compare to the mft entry (string)
        :return: file's name is equal to filename
        """

        if not self.is_valid():
            return False

        filename_attribute = self.mft_parser.get_attribute(FILE_NAME_TYPE, self)

        if filename_attribute == NO_SUCH_ATTRIBUTE:
            return False

        try:
            # Extracting the filename from the mft entry
            extracted_filename = self.mft_parser.parse_filename(filename_attribute).decode()

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

        return b'FILE' == self.entry[:0x4] and b'\x30\x00\x00\x00' in self.entry
