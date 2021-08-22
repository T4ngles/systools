"""
    System health check
    to add:
        File Backup
        System component health check
        System Internal traffic monitor
        System External traffic monitor
        File integrity (Start up and Shutdown scheduled check)
            -recursive loop for all directories and files below target
            -store of hash result in dictionary
            -encryption of hash result
            -export of file hash dictionary
            -encryption of dictionary
            -decryption of dictionary
            -length comparison of dictionary to current files
                -list new files and hashes
            -comparison of dictionary to current files
"""

import hashlib
import sys
import os
import file_walker
import file_hasher
import csv


def main():
    
    walk_dir = os.path.dirname(sys.argv[0])
    for file in file_walker.raywalk(walk_dir):
        file_hash = general_hasher(file)
        print('general hash:',general_hasher(file))
    
if __name__ == '__main__':
    main()
