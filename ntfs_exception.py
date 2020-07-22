class NTFSException(Exception):
    pass


class FileNotFoundException(NTFSException):
    pass


class AttributeNotFoundException(NTFSException):
    pass
