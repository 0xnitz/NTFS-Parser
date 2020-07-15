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

        if self.mft_parser.is_resident(self.mft_parser.get_attribute(DATA_TYPE, self)):
            return self.mft_parser.parse_data(self.mft_parser.get_attribute(DATA_TYPE, self))

        return b'This $DATA is non-resident!'

    def __eq__(self, filename):
        """
        This function will compare between a filename and the MFT Entry's $FILE_NAME attribute
        :param filename: filename to compare to the mft entry (string)
        :return: file's name is equal to filename
        """

        # Extracting the filename from the mft entry
        extracted_filename = self.mft_parser.parse_filename(
            self.mft_parser.get_attribute(FILE_NAME_TYPE, self)).decode()

        # Removing the extra null bytes between each char
        extracted_filename = ''.join(extracted_filename.split('\x00'))

        # Checking to see if we found the file
        return extracted_filename == filename
