from constants import DATA_TYPE, FILE_NAME_TYPE, FILE_NAME_TYPE_BYTES, MFT_ENTRY_MAGIC, ENTRY_INUSE
from file_name_attribute import FileNameAttribute
from attribute_parser import AttributeParser
from ntfs_exception import NTFSException
from data_attribute import DataAttribute


class MFTEntry:
    def __init__(self, entry):
        self.entry = entry

    def read_resident_data(self):
        data_attribute = AttributeParser.get_attribute(DATA_TYPE, self)
        return AttributeParser.parse_data(data_attribute)

    def get_data(self, sectors_per_cluster, vbr_offset):
        return DataAttribute(AttributeParser.get_attribute(DATA_TYPE, self),
                             sectors_per_cluster, vbr_offset).get_data()

    def get_filename(self):
        if not self.is_valid():
            raise NTFSException

        return FileNameAttribute(AttributeParser.get_attribute(FILE_NAME_TYPE, self)).get_data()

    def is_valid(self):
        return MFT_ENTRY_MAGIC == self.entry[:0x4] and \
               FILE_NAME_TYPE_BYTES in self.entry and self.entry[ENTRY_INUSE]
