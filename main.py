
"""Read a single sector of a physical disk. Tested on Mac OS 10.13.3 and Windows 8."""

import os
import sys
import struct


def main():  # Read the first sector of the first disk as example.
    sector = 0
    sample_mft = open('sample_mft.bin', 'wb')
    for sector in range(5000):
        data = read_sector(r'\\.\physicaldrive0', sector)
        if b'FILE' in data:
            print(sector, data)
            sample_mft.write(data)

    #for sector in range(10000):
    #    data = read_sector(r'\\.\physicaldrive0', sector)
    #    if b'FILE' in data:
    #        print(sector, data)

def read_sector(disk, sector_no=0, amount=1):
    """Read a single sector of the specified disk.
    Keyword arguments:
    disk -- the physical ID of the disk to read.
    sector_no -- the sector number to read (default: 0).
    """
    # Static typed variable
    read = None
    # File operations with `with` syntax. To reduce file handling efforts.
    with open(disk, 'rb') as fp:
        fp.seek(sector_no * 512)
        read = fp.read(512 * amount)
    return read


if __name__ == "__main__":
    main()
