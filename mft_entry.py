from attribute_parser import *
from constants import DATA_TYPE, FILE_NAME_TYPE, UNALLOCATED_ENTRY, NO_SUCH_ATTRIBUTE, FILE_NAME_TYPE_BYTES
from ntfs_exception import NTFSException


class MFTEntry:
    """
    This class represents an MFTEntry.
    """

    def __init__(self, entry):
        self.entry = entry

    # CR: [design] How does it make sense that read_resident_data is a function
    # of MFTEntry but read_non_resident_data is not? Moreover, wouldn't it make
    # sense for MFTEntry to expose a read_data() function instead? Why should
    # client classes care if the data is resident or not?
    def read_resident_data(self):
        """
        Read the data attribute using the MFTParser class
        :return: data attribute contents
        """

        # Cut the $DATA attribute from the entry
        data_attribute = AttributeParser.get_attribute(DATA_TYPE, self)

        # If the $DATA attribute is resident, parse and print it's data
        return AttributeParser.parse_data(data_attribute)

    # CR: [design] This is a confusing choice. It is non-intuitive to compare
    # an entry to a file name. You should use accessors to export the file
    # name to clients, and then they can compare file names.
    def get_filename(self):
        """
        This function will compare between a filename and the MFT Entry's $FILE_NAME attribute
        :param filename: filename to compare to the mft entry (string)
        :return: file's name is equal to filename
        """

        # Checking if the entry is a valid MFT entry
        if not self.is_valid():
            raise NTFSException

        # Cutting the $FILE_NAME attribute from the entry
        filename_attribute = AttributeParser.get_attribute(FILE_NAME_TYPE, self)

        # Extracting the filename from the mft entry
        return AttributeParser.parse_filename(filename_attribute).decode('utf-16le')

    def is_valid(self):
        """
        This function validates an MFT entry.
        *The entry has the FILE signature
        *The entry has a FILE_NAME attribute
        :return: True/False is the entry valid for parsing
        """

        # Checking if the entry has the signature and a $FILE_NAME attribute
        return b'FILE' == self.entry[:0x4] and FILE_NAME_TYPE_BYTES in self.entry

