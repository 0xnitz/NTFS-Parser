**NTFS Parser**

This is a NTFS Parser written in python3.

The program will find the MFT, iterate over it's listings and their $FILE_NAME. When the correct file is found it's $DATA attribute will be printed.

**Usage**
```diff
$ python3 main.py [filename]
...
File found/not found!
File's contents:
...
```

@Nitzan Adut
