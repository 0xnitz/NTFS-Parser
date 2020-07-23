ATTRIBUTE_NON_RESIDENT_FLAG_OFFSET = 0x8


class Attribute:
    def __init__(self, attribute_bytes):
        self.attribute_bytes = attribute_bytes

    def is_resident(self):
        return not self.attribute_bytes[ATTRIBUTE_NON_RESIDENT_FLAG_OFFSET]

    # CR: [design] The concept of resident and non-resident data should be
    # handled by this class, as this is a behaviour that is common to all
    # attributes. Specializations of the class should only have to deal with
    # parsing the data itself.
    def get_data(self):
        pass
