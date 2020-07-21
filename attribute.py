ATTRIBUTE_NON_RESIDENT_FLAG_OFFSET = 0x8


class Attribute:
    def __init__(self, attribute_bytes):
        self.attribute_bytes = attribute_bytes

    def is_resident(self):
        return not self.attribute_bytes[ATTRIBUTE_NON_RESIDENT_FLAG_OFFSET]

    def get_data(self):
        pass
