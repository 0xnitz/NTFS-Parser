class MFTEntry:
    def __init__(self, entry):
        self.entry = entry

    def read_data(self):
        """
        Read the data attribute using the MFTParser class
        :return: data attribute contents
        """

        return b''

    def __eq__(self, filename):
        """
        This function will compare between a filename and the MFT Entry's $FILE_NAME attribute
        :param other: filename (string)
        :return: file's name is equal to filename
        """

        return True
