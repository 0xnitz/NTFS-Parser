# CR: [conventions] Order imports by length
from attribute_parser import AttributeParser
from mft_entry import MFTEntry
# CR: [conventions] Don't use star imports
from ntfs_handler import *
from sector_reader import SectorReader
from constants import *


class NTFSParser:
    # CR: [finish] Docstrings should be written for end users. Something like
    # "Gives access to file contents in an NTFS filesystem". In general it is
    # tempting to start with "this class" or "this function", but these phrases
    # are obvious in the context where they are written.
    """
    This class represents my NTFSParser, it controls all the other objects.
    The parser locates the MFT from the VBR and iterates over it,
    parsing it until it finds an entry with the same filename.
    """

    def __init__(self):
        # CR: [finish] This is unused, remove
        self.mft_parser = AttributeParser()
        self.handler = NTFSHandler()

        # Locating the largest partition on the disk (C:) and setting VBR_OFFSET to the vbr of C:
        self.handler.locate_partition()

        # Finding the MFT sector offset using the VBR
        self.handler.find_mft()

    # CR: [finish] This function doesn't return a file, but its content. The
    # name should reflect that.
    # CR: [design] Or... split the functionality of finding a file from
    # printing its data.
    def find_file(self, filename):
        # CR: [finish] The function returns raw data, which is not the same as
        # a data attribute. Be precise!
        # CR: [finish] Don't leave blank fields in the docstring. Either fill
        # or remove them.
        """
        This function iterates over every MFT entry and compares it's FILE_NAME to the filename parameter.
        If the program found the right file, it returns it's data attribute
        :param filename:
        :return:
        """

        # Iterating over the MFT and searching for the filename
        current_entry = MFTEntry(self.handler.get_next_entry())
        # CR: [design] These lines are filled with strange interface choices:
        # 1. MFTEntry should implement __len__ itself to encapsulate its
        # members.
        # 2. Even better in this case would be to provide an is_valid property.
        # 3. It should also implement .file_name accessor rather than the
        # non-trivial __eq__.
        # 4. The stop condition should also be more explicit, and can be better
        # done by implementing NTFSHandler.has_next(), or simply by making it
        # iterable (using __iter__ and __next__).
        while len(current_entry.entry) > 0:
            # Using the __eq__ operator of MFTEntry to check if the entry has the correct filename
            if current_entry == filename:
                return self.handler.read_data(current_entry)
            current_entry.entry = self.handler.get_next_entry()

            if current_entry.entry == READ_ENTIRE_MFT:
                break

        # After iterating after the whole MFT, file not found
        # CR: [design] Use exceptions! What if a file's content is equal to
        # failure? If you are returning a bytes object the only legit way to
        # signal a failure is by raising.
        return FAILURE
