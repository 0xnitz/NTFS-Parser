from constants import FILE_NAME_LENGTH, FILE_NAME_DATA, DATA_LENGTH, DATA_ATTRIBUTE_DATA, ENTRY_INUSE,\
    FIRST_ATTRIBUTE_OFFSET, END_OF_ENTRY, IS_NON_RESIDENT_ATTRIBUTE
from ntfs_exception import AttributeNotFoundException, NTFSException

from struct import unpack


# CR: [design] You have so many ways to use this interface incorrectly. For
# example calling parse_filename on a data attribute. Make your interfaces easy
# to use correctly and hard to use incorrectly.
class AttributeParser:
    # CR: [finish] This comment uses the wrong class name!
    # CR: [design] If all these functions are independent of class objects then:
    # 1. Make it illegal to create objects (raise an exception in __init__)
    # 2. Use the @staticmethod decorator
    """
    These function don't need a class, they can be static functions.
    I chose to put them in the MFTParser class to group functions that parse mft entries together.
    """

    def __init__(self):
        raise NTFSException

    # CR: [design] If this is a parsing function, why not return the data in
    # the most suitable type (string)?
    @staticmethod
    def parse_filename(attribute):
        """
        Extracts the actual filename from the $FILE_NAME attribute
        :param attribute: The binary attribute from the MFT
        :return: The filename in bytes
        """

        # Extracting the filename from the $FILE_NAME attribute
        length_in_bytes = attribute[FILE_NAME_LENGTH] * 2
        return attribute[FILE_NAME_DATA:FILE_NAME_DATA+length_in_bytes]

    @staticmethod
    def parse_data(attribute):
        """
        Extracts the actual data from the $DATA attribute
        :param attribute: The binary attribute from the MFT
        :return: The $DATA contents
        """

        # Extracting the data from the resident $DATA attribute
        length = unpack('I', attribute[DATA_LENGTH:DATA_LENGTH+4])[0]
        return attribute[DATA_ATTRIBUTE_DATA:DATA_ATTRIBUTE_DATA+length]

    @staticmethod
    def get_attribute(attribute_code, mft_entry):
        """
        This function will receive an attribute code and an mft entry and will return the attribute's data
        :param attribute_code: attribute code in the mft
        :param mft_entry: MFTEntry object
        :return: attribute's data
        """

        # If the in-use flag is 0 the entry is un allocated
        # CR: [design] Raise exceptions in illegal states
        if not mft_entry.entry[ENTRY_INUSE]:
            raise NTFSException

        # If the directory flag is 1 the entry is a directory, we're looking for a file
        # CR: [design] Is this the place to make such decisions? What happens
        # when the requirements specify directories as well?

        # Unpack the offset of the first attribute from the start of the entry
        offset = unpack('H', mft_entry.entry[FIRST_ATTRIBUTE_OFFSET:FIRST_ATTRIBUTE_OFFSET+2])[0]
        while offset < len(mft_entry.entry):
            # Unpack the current attribute length and attribute type
            attribute_len = unpack('I', mft_entry.entry[offset+4:offset+8])[0]
            current_attribute_code = unpack('I', mft_entry.entry[offset:offset+4])[0]

            # Attribute isn't the one we're looking for
            if current_attribute_code != attribute_code:
                # End of MFT Entry, attribute not found
                if current_attribute_code == END_OF_ENTRY:
                    raise AttributeNotFoundException

                # Jump to the next attribute
                offset += attribute_len
                continue

            # If the attribute is found, return it
            return mft_entry.entry[offset:offset+attribute_len]

        # Attribute not found in entry
        raise AttributeNotFoundException

    @staticmethod
    def is_resident(attribute):
        """
        This function checks if an attribute's data is resident by checking the non-resident flag
        :param attribute: The binary attribute
        :return: True/False not on the flag
        """

        return not attribute[IS_NON_RESIDENT_ATTRIBUTE]
