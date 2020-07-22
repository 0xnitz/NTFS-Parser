**NTFS Parser**

This is a NTFS Parser written in python3.

The program will find the MFT, iterate over it's listings and their $FILE_NAME. When the correct file is found it's $DATA attribute will be printed.

**Usage**

(1) Open the command line as an admin

(2) 
```diff
$ python3 main.py hosts
[] Searching for file hosts...
[] Found it!
hosts' contents:

b"# Copyright (c) 1993-2009 Microsoft Corp.\r\n#\r\n# This is a sample HOSTS file ..."

[] Parser finished execution, runtime -> 2.236306667327881s...
```

@Nitzan Adut
