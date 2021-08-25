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
import datetime


def main():
    verbose = False

    if verbose:
        def vprint(*args):
            for arg in args:
                print(arg)
    else:
        def vprint(*args):
            pass
        
    file_hash_dict_list = []
    
    walk_dir = os.path.dirname(sys.argv[0])
    for file in file_walker.raywalk(walk_dir,verbose):
        file_hash = file_hasher.general_hasher(file)
        file_hash_dict = {"hash":file_hash,"filename":os.path.basename(file),"filepath":file}
        file_hash_dict_list.append(file_hash_dict)
        vprint('general hash:', file_hash)

    with open(str(datetime.date.today())+'-file_hash_dict.csv', 'w', newline='') as csvfile:
        fieldnames = ["hash", "filename", "filepath"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in file_hash_dict_list:
            writer.writerow(item)
            print(item["hash"],item["filename"])
        
        
if __name__ == '__main__':
    main()
