from ntfs_exception import AttributeNotFoundException, NTFSException

from struct import unpack

# CR: [design] Constants should belong to a class
FIRST_ATTRIBUTE_OFFSET_IN_ENTRY = 0x14
ENTRY_INUSE_FLAG_OFFSET = 0x16
END_OF_ENTRY = 0xffffffff


class AttributeParser:
    def __init__(self):
        raise NTFSException

    # CR: [finish] Rename to get_attributes
    # CR: [implementation] Break this function down
    @staticmethod
    def get_attribute(attribute_code, mft_entry):
        # CR: [finish] Rename to attributes
        attribute = []
        entry = mft_entry.get_entry()
        offset = unpack('H', entry[FIRST_ATTRIBUTE_OFFSET_IN_ENTRY:FIRST_ATTRIBUTE_OFFSET_IN_ENTRY + 2])[0]

        while offset < len(entry):
            attribute_len = unpack('I', entry[offset+4:offset+8])[0]
            current_attribute_code = unpack('I', entry[offset:offset+4])[0]

            if current_attribute_code != attribute_code:
                if current_attribute_code == END_OF_ENTRY:
                    if len(attribute) > 0:
                        return attribute

                    # CR: [design] There's no need for an exception here. An
                    # empty list will suffice.
                    raise AttributeNotFoundException

                offset += attribute_len
                continue

            attribute.append(entry[offset:offset+attribute_len])
            offset += attribute_len

        if len(attribute) > 0:
            return attribute

        raise AttributeNotFoundException
