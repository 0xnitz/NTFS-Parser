import struct
from constants import *


class AttributeParser:
    """
    These function don't need a class, they can be static functions.
    I chose to put them in the MFTParser class to group functions that parse mft entries together.
    """

    def __init__(self):
        pass

    def parse_filename(self, attribute):
        """
        Extracts the actual filename from the $FILE_NAME attribute
        :param attribute: The binary attribute from the MFT
        :return: The filename in bytes
        """

        # Extracting the filename from the $FILE_NAME attribute
        length_in_bytes = attribute[FILE_NAME_LENGTH] * 2
        return attribute[FILE_NAME_DATA:FILE_NAME_DATA+length_in_bytes]

    def parse_data(self, attribute):
        """
        Extracts the actual data from the $DATA attribute
        :param attribute: The binary attribute from the MFT
        :return: The $DATA contents
        """

        # Extracting the data from the resident $DATA attribute
        length = struct.unpack('I', attribute[DATA_LENGTH:DATA_LENGTH+4])[0]
        return attribute[DATA_ATTRIBUTE_DATA:DATA_ATTRIBUTE_DATA+length]

    def get_attribute(self, attribute_code, mft_entry):
        """
        This function will receive an attribute code and an mft entry and will return the attribute's data
        :param attribute_code: attribute code in the mft
        :param mft_entry: MFTEntry object
        :return: attribute's data
        """

        # If the in-use flag is 0 the entry is un allocated
        if not mft_entry.entry[ENTRY_INUSE]:
            return UNALLOCATED_ENTRY

        # If the directory flag is 1 the entry is a directory, we're looking for a file
        if mft_entry.entry[ENTRY_DIRECTORY]:
            return DIRECTORY

        # Unpack the offset of the first attribute from the start of the entry
        offset = struct.unpack('H', mft_entry.entry[FIRST_ATTRIBUTE_OFFSET:FIRST_ATTRIBUTE_OFFSET+2])[0]
        while offset < len(mft_entry.entry):
            # Unpack the current attribute length and attribute type
            attribute_len = struct.unpack('I', mft_entry.entry[offset+4:offset+8])[0]
            current_attribute_code = struct.unpack('I', mft_entry.entry[offset:offset+4])[0]

            # Attribute isn't the one we're looking for
            if current_attribute_code != attribute_code:
                # End of MFT Entry, attribute not found
                if current_attribute_code == END_OF_ENTRY:
                    return NO_SUCH_ATTRIBUTE

                # Jump to the next attribute
                offset += attribute_len
                continue

            # If the attribute is found, return it
            return mft_entry.entry[offset:offset+attribute_len]

        # Attribute not found in entry
        return NO_SUCH_ATTRIBUTE

    def is_resident(self, attribute):
        """
        This function checks if an attribute's data is resident by checking the non-resident flag
        :param attribute: The binary attribute
        :return: True/False not on the flag
        """

        return not attribute[IS_NON_RESIDENT_ATTRIBUTE]
