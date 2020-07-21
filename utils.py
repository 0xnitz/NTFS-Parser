from struct import unpack


def bytes_to_number(bytes_object):
    """
    This function takes in a bytes object and converts it to a number (1-8 length)
    :param bytes_object: The bytes object to convert
    :return: The result
    """

    bytes_object_length = len(bytes_object)

    if len(bytes_object) > 8:
        raise ValueError

    if bytes_object_length == 1:
        return bytes_object[0]
    elif bytes_object_length == 2:
        return unpack('H', bytes_object)[0]
    elif 2 < bytes_object_length <= 4:
        # CR: [requirements] Are you allowed to assume endianity?
        bytes_object += b'\x00' * (4 - bytes_object_length)
        return unpack('I', bytes_object)[0]
    elif 4 < bytes_object_length <= 8:
        bytes_object += b'\x00' * (8 - bytes_object_length)
        return unpack('Q', bytes_object)[0]
