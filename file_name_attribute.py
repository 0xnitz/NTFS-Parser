from constants import FILE_NAME_LENGTH, FILE_NAME_DATA
from ntfs_exception import NTFSException
from attribute import Attribute


class FileNameAttribute(Attribute):
    def __init__(self, attribute_bytes):
        super().__init__(attribute_bytes)

    def get_data(self):
        if self.is_resident():
            length_in_bytes = self.attribute_bytes[FILE_NAME_LENGTH] * 2
            return self.attribute_bytes[FILE_NAME_DATA:FILE_NAME_DATA + length_in_bytes].decode('utf-16le')
        else:
            raise NTFSException
