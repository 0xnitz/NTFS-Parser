from attribute_parser import AttributeParser, ENTRY_INUSE_FLAG_OFFSET
from file_name_attribute import FileNameAttribute
from data_attribute import DataAttribute
from ntfs_exception import NTFSException

FILE_NAME_TYPE = 0x30
DATA_TYPE = 0x80
FILE_NAME_TYPE_BYTES = b'\x30\x00\x00\x00'
MFT_ENTRY_MAGIC = b'FILE'
MFT_ENTRY_SIZE = 1024


class MFTEntry:
    def __init__(self, entry):
        self.entry = entry

    def get_data(self, sectors_per_cluster, vbr_offset, read_in_parts=False, run_index=0):
        return DataAttribute(AttributeParser.get_attribute(DATA_TYPE, self),
                             sectors_per_cluster, vbr_offset).get_data(
            read_in_parts=read_in_parts, run_index=run_index)

    def get_filename(self):
        if not self.is_valid():
            raise NTFSException

        return FileNameAttribute(AttributeParser.get_attribute(FILE_NAME_TYPE, self)).get_data()

    def is_valid(self):
        return MFT_ENTRY_MAGIC == self.entry[:0x4] and \
               FILE_NAME_TYPE_BYTES in self.entry and self.entry[ENTRY_INUSE_FLAG_OFFSET]
