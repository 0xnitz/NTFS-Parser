from sector_reader import SectorReader, SECTOR_SIZE
from mft_entry import MFTEntry, MFT_ENTRY_SIZE
from physical_drive import PhysicalDrive
from data_run import DRIVE_NUMBER


class MFTLoader:
    def __init__(self):
        self.drive = PhysicalDrive(DRIVE_NUMBER)
        self.sector_reader = SectorReader(r'\\.\physicaldrive' + str(DRIVE_NUMBER))
        self.run_index = 0
        self.mft = self.load_mft()

    def load_mft(self):
        mft_entry = self.sector_reader.read_from(self.drive.locate_largest_partition_mft_starting_sector()
                                                 + self.drive.locate_largest_partition_vbr_offset(),
                                                 round(MFT_ENTRY_SIZE / SECTOR_SIZE))

        self.mft = MFTEntry(mft_entry).get_data(self.drive.locate_largest_partition_sectors_per_cluster(),
                                                self.drive.locate_largest_partition_vbr_offset(),
                                                read_in_parts=True, run_index=self.run_index)

        self.run_index += 1

        return self.mft
