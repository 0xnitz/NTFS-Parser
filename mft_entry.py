from ntfs_exception import AttributeNotFoundException
from file_name_attribute import FileNameAttribute
from attribute_parser import AttributeParser
from data_attribute import DataAttribute

FILE_NAME_TYPE = 0x30
DATA_TYPE = 0x80
MFT_ENTRY_MAGIC = b'FILE'
MFT_ENTRY_SIZE = 1024


class MFTEntry:
    def __init__(self, entry):
        self.entry = entry

    def get_data(self, disk, sectors_per_cluster, read_in_parts=False, run_index=0):
        try:
            data_attributes = AttributeParser.get_attribute(DATA_TYPE, self)
        except AttributeNotFoundException:
            return b''

        data = b''

        for data_attribute in data_attributes:
            data += DataAttribute(data_attribute, sectors_per_cluster)\
                .get_data(disk, read_in_parts=read_in_parts, run_index=run_index)

        return data

    def get_file_names(self):
        file_name_attributes = AttributeParser.get_attribute(FILE_NAME_TYPE, self)

        return [FileNameAttribute(file_name).get_data() for file_name in file_name_attributes]

    def get_entry(self):
        return self.entry

    def is_valid(self):
        return MFT_ENTRY_MAGIC == self.entry[:0x4]
