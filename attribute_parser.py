from ntfs_exception import NTFSException

from struct import unpack


class AttributeParser:
    ENTRY_INUSE_FLAG_OFFSET = 0x16
    END_OF_ENTRY = 0xffffffff

    def __init__(self):
        raise NTFSException()

    @staticmethod
    def get_attributes(attribute_code, mft_entry):
        attributes = []
        attributes_raw = mft_entry.get_attributes_raw_data()
        offset = 0

        while offset < len(attributes_raw):
            current_attribute_code = unpack('I', attributes_raw[offset:offset + 4])[0]
            attribute_len = unpack('I', attributes_raw[offset+4:offset+8])[0]

            if current_attribute_code != attribute_code:
                if current_attribute_code == AttributeParser.END_OF_ENTRY:
                    return attributes

                offset += attribute_len
                continue

            attributes.append(attributes_raw[offset:offset+attribute_len])
            offset += attribute_len

            return attributes
