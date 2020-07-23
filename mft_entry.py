from ntfs_exception import AttributeNotFoundException
from file_name_attribute import FileNameAttribute
from attribute_parser import AttributeParser
from data_attribute import DataAttribute

from struct import unpack


class MFTEntry:
    FILE_NAME_TYPE = 0x30
    DATA_TYPE = 0x80
    MFT_ENTRY_MAGIC = b'FILE'
    MFT_ENTRY_SIZE = 1024
    FIRST_ATTRIBUTE_OFFSET_IN_ENTRY = 0x14

    def __init__(self, entry):
        self._entry = entry

    def get_data(self, disk, sectors_per_cluster, read_in_parts=False, run_index=0):
        data_attributes = AttributeParser.get_attributes(MFTEntry.DATA_TYPE, self)
        data = b''

        for data_attribute in data_attributes:
            data += DataAttribute(data_attribute, sectors_per_cluster)\
                .get_data(disk, read_in_parts=read_in_parts, run_index=run_index)

        return data

    def get_file_names(self):
        file_name_attributes = AttributeParser.get_attributes(MFTEntry.FILE_NAME_TYPE, self)
        if not file_name_attributes:
            raise AttributeNotFoundException()

        return [FileNameAttribute(file_name).get_data() for file_name in file_name_attributes]

    def get_attributes_raw_data(self):
        return self._entry[unpack('H', self._entry[MFTEntry.FIRST_ATTRIBUTE_OFFSET_IN_ENTRY:
                                                   MFTEntry.FIRST_ATTRIBUTE_OFFSET_IN_ENTRY + 2])[0]:]

    def is_valid(self):
        try:
            self.get_file_names()
        except AttributeNotFoundException:
            return False

        return MFTEntry.MFT_ENTRY_MAGIC == self._entry[:0x4]
