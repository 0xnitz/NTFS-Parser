IS_NON_RESIDENT_ATTRIBUTE = 0x8


class Attribute:
    def __init__(self, attribute_bytes):
        self.attribute_bytes = attribute_bytes

    def is_resident(self):
        return not self.attribute_bytes[IS_NON_RESIDENT_ATTRIBUTE]

    def get_data(self):
        pass
