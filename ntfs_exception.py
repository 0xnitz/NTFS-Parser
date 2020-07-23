class NTFSException(Exception):
    pass


class FileNotFoundException(NTFSException):
    pass


class AttributeNotFoundException(NTFSException):
    pass


class DiskDoesNotExist(NTFSException):
    pass
