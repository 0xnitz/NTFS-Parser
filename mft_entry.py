from mft_parser import MFTParser

FILE_NAME_TYPE = 0x30
DATA_TYPE = 0x80


class MFTEntry:
    def __init__(self, entry):
        self.entry = entry
        self.parser = MFTParser()

    def read_data(self):
        """
        Read the data attribute using the MFTParser class
        :return: data attribute contents
        """

        return self.parser.get_attribute(DATA_TYPE, self.entry)

    def __eq__(self, filename):
        """
        This function will compare between a filename and the MFT Entry's $FILE_NAME attribute
        :param other: filename (string)
        :return: file's name is equal to filename
        """

        return self.parser.get_attribute(FILE_NAME_TYPE, self.entry).decode() == filename
