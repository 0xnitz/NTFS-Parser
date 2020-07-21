class NTFSException(Exception):
    pass


class ReadEntireMFTException(NTFSException):
    pass


class FileNotFoundException(NTFSException):
    pass


class AttributeNotFoundException(NTFSException):
    pass
