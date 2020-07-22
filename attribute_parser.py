from ntfs_exception import AttributeNotFoundException, NTFSException

from struct import unpack

FIRST_ATTRIBUTE_OFFSET_IN_ENTRY = 0x14
END_OF_ENTRY = 0xffffffff
ENTRY_INUSE_FLAG_OFFSET = 0x16


class AttributeParser:
    def __init__(self):
        raise NTFSException

    @staticmethod
    def get_attribute(attribute_code, mft_entry):
        attribute = []
        offset = unpack('H', mft_entry.entry[FIRST_ATTRIBUTE_OFFSET_IN_ENTRY:FIRST_ATTRIBUTE_OFFSET_IN_ENTRY + 2])[0]
        while offset < len(mft_entry.entry):
            attribute_len = unpack('I', mft_entry.entry[offset+4:offset+8])[0]
            current_attribute_code = unpack('I', mft_entry.entry[offset:offset+4])[0]

            if current_attribute_code != attribute_code:
                if current_attribute_code == END_OF_ENTRY:
                    if len(attribute) > 0:
                        return attribute

                    raise AttributeNotFoundException

                offset += attribute_len
                continue

            attribute.append(mft_entry.entry[offset:offset+attribute_len])
            offset += attribute_len

        if len(attribute) > 0:
            return attribute

        raise AttributeNotFoundException
