"""
I grouped all the constants in one file because some
constants are relevant to multiple classes.
"""

# CR: [finish] Sometimes constants really are relevant to multiple parts of the
# program. This doesn't necessarily mean they do not belong to a specific
# entity. For example END_OF_ENTRY seems to belong to a MFTEntry entity. This
# doesn't make it inaccessible, just gives it context since it will be used as
# MFTEntry.END_OF_ENTRY. Not giving such context might lead to greater
# confusion, especially when certain constants may exist in the context of many
# entities.
UNALLOCATED_ENTRY = b'\x01'
NO_SUCH_ATTRIBUTE = b'\x02'
FAILURE = b'\x01'
READ_ENTIRE_MFT = b'\xff'
FILE_NAME_TYPE = 0x30
DATA_TYPE = 0x80
SECTOR_SIZE = 512
MFT_ENTRY_SIZE = 1024
VBR_OFFSET = 0
# CR: [implementation] Wouldn't it make way more sense to work with powers of
# 2?
CHUNK_SIZE = 1000
FILE_NAME_LENGTH = 0x58
FILE_NAME_DATA = 0x5a
DATA_LENGTH = 0x10
DATA_ATTRIBUTE_DATA = 0x18
ENTRY_INUSE = 0x16
ENTRY_DIRECTORY = 0x17
# CR: [requirements] Are you allowed to assume this is constant?
FIRST_ATTRIBUTE_OFFSET = 0x14
END_OF_ENTRY = 0xffffffff
IS_NON_RESIDENT_ATTRIBUTE = 0x8
RUN_LIST_OFFSET = 0x20
SECTOR_SIZE_OFFSET = 0xb
SECTORS_PER_CLUSTER_OFFSET = 0xd
MFT_START_SECTOR_OFFSET = 0x30
FILE_NAME_TYPE_BYTES = b'\x30\x00\x00\x00'
OEM_ID = b'NTFS'
MFT_ENTRY_MAGIC = b'FILE'
