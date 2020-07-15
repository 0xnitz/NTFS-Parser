import struct
from constants import *


class MFTParser:
    def __init__(self):
        pass

    def parse_filename(self, attribute):
        """
        Extracts the actual filename from the $FILE_NAME attribute
        :param attribute: The binary attribute from the MFT
        :return: The filename in bytes
        """

        length_in_bytes = attribute[0x58] * 2
        return attribute[0x5a:0x5a+length_in_bytes]

    def parse_data(self, attribute):
        """
        Extracts the actual data from the $DATA attribute
        :param attribute: The binary attribute from the MFT
        :return: The $DATA contents
        """

        length = struct.unpack('I', attribute[0x10:0x14])[0]
        return attribute[0x18:0x18+length]

    def get_attribute(self, attribute_code, mft_entry):
        """
        This function will receive an attribute code and an mft entry and will return the attribute's data
        :param attribute_code: attribute code in the mft
        :param mft_entry: MFTEntry object
        :return: attribute's data
        """

        if not mft_entry.entry[0x16]:
            return UNALLOCATED_ENTRY

        offset = struct.unpack('H', mft_entry.entry[0x14:0x16])[0]
        while offset < len(mft_entry.entry):
            attribute_len = struct.unpack('I', mft_entry.entry[offset+4:offset+8])[0]
            current_attribute_code = struct.unpack('I', mft_entry.entry[offset:offset+4])[0]
            if current_attribute_code != attribute_code:
                offset += attribute_len
                continue

            return mft_entry.entry[offset:offset+attribute_len]

        return NO_SUCH_ATTRIBUTE

    def is_resident(self, attribute):
        return not attribute[0x08]
