from constants import MFT_ENTRY_SIZE, SECTOR_SIZE, DATA_TYPE
from attribute_parser import AttributeParser
from physical_drive import PhysicalDrive
from sector_reader import SectorReader
from mft_entry import MFTEntry
from run_list import RunList


class MFTLoader:
    def __init__(self):
        self.drive = PhysicalDrive(0)
        self.sector_reader = SectorReader(r'\\.\physicaldrive0')

    def load_mft(self):
        mft_entry = self.sector_reader.read_from(self.drive.locate_largest_partition_mft_starting_sector()
                                                 + self.drive.locate_largest_partition_vbr_offset(),
                                                 round(MFT_ENTRY_SIZE / SECTOR_SIZE))
        data_attribute = AttributeParser.get_attribute(DATA_TYPE, MFTEntry(mft_entry))
        return RunList(data_attribute[data_attribute[0x20]:], self.drive.locate_largest_partition_sectors_per_cluster(),
                       self.drive.locate_largest_partition_vbr_offset()).read_all_runs()

