from constants import FILE_NAME_LENGTH, FILE_NAME_DATA, DATA_LENGTH, DATA_ATTRIBUTE_DATA, ENTRY_INUSE,\
    FIRST_ATTRIBUTE_OFFSET, END_OF_ENTRY, IS_NON_RESIDENT_ATTRIBUTE
from ntfs_exception import AttributeNotFoundException, NTFSException

from struct import unpack


class AttributeParser:
    def __init__(self):
        raise NTFSException

    @staticmethod
    def parse_filename(attribute):
        length_in_bytes = attribute[FILE_NAME_LENGTH] * 2
        return attribute[FILE_NAME_DATA:FILE_NAME_DATA+length_in_bytes]

    @staticmethod
    def parse_data(attribute):
        length = unpack('I', attribute[DATA_LENGTH:DATA_LENGTH+4])[0]
        return attribute[DATA_ATTRIBUTE_DATA:DATA_ATTRIBUTE_DATA+length]

    @staticmethod
    def get_attribute(attribute_code, mft_entry):
        if not mft_entry.entry[ENTRY_INUSE]:
            raise NTFSException

        offset = unpack('H', mft_entry.entry[FIRST_ATTRIBUTE_OFFSET:FIRST_ATTRIBUTE_OFFSET+2])[0]
        while offset < len(mft_entry.entry):
            attribute_len = unpack('I', mft_entry.entry[offset+4:offset+8])[0]
            current_attribute_code = unpack('I', mft_entry.entry[offset:offset+4])[0]

            if current_attribute_code != attribute_code:
                if current_attribute_code == END_OF_ENTRY:
                    raise AttributeNotFoundException

                offset += attribute_len
                continue

            return mft_entry.entry[offset:offset+attribute_len]

        raise AttributeNotFoundException

    @staticmethod
    def is_resident(attribute):
        return not attribute[IS_NON_RESIDENT_ATTRIBUTE]
