from sector_reader import SectorReader, SECTOR_SIZE
from mft_entry import MFTEntry, MFT_ENTRY_SIZE
from physical_drive import PhysicalDrive


class MFTLoader:
    def __init__(self):
        self.drive = PhysicalDrive(0)
        self.sector_reader = SectorReader(r'\\.\physicaldrive' + str(0))
        self.mft = self._load_mft()

    def _load_mft(self):
        mft_entry = self.sector_reader.read_from(self.drive.locate_largest_partition_mft_starting_sector()
                                                 + self.drive.locate_largest_partition_vbr_offset(),
                                                 round(MFT_ENTRY_SIZE / SECTOR_SIZE))

        return MFTEntry(mft_entry).get_data(self.drive.locate_largest_partition_sectors_per_cluster(),
                                            self.drive.locate_largest_partition_vbr_offset())
