from ntfs_exception import AttributeNotFoundException, NTFSException
from attribute import IS_NON_RESIDENT_ATTRIBUTE

from struct import unpack

FIRST_ATTRIBUTE_OFFSET = 0x14
END_OF_ENTRY = 0xffffffff
ENTRY_INUSE = 0x16


class AttributeParser:
    def __init__(self):
        raise NTFSException

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
