"""
    System health check
    to add:
        File Backup
        System component health check
        System Internal traffic monitor
        System External traffic monitor
        File integrity (Start up and Shutdown scheduled check)
            -include progress bar of walk through files
            -improve walk speed
            -encryption of dictionary
            -decryption of dictionary
            -loading previous stored dictionary and comparison during hash flagging whether hash is same or not using name as key
            -length comparison of dictionary to current files
                -list new files and hashes
            -comparison of dictionary to current files
            -export file change summary
            -visualisation of changes
"""

import hashlib
import sys
import os
import file_walker
import file_hasher
import csv
import datetime
import time

def debug_block_heading(title):
    title_length = len(title)
    block_size = 50
    spacer = "="*int((block_size-title_length)/2-1)
    spacer_length = len(spacer)+1
    leftover = block_size-2*spacer_length-title_length
    vprint("="*block_size)
    vprint(spacer,title,spacer,"="*leftover)
    vprint("="*block_size)

def main():
    
    start_date = datetime.datetime.now()
    
    verbose = False

    if verbose:
        def vprint(*args):
            for arg in args:
                print(arg)
    else:
        def vprint(*args):
            pass
        
    file_hash_dict_list = []
    
    walk_dir = os.path.splitdrive(sys.argv[0])[0] + "\\"#C drive #os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0])))) #Documents folder #os.path.dirname(sys.argv[0]) #file_integrity folder
    debug_block_heading("File Integrity Check of " + walk_dir)
    startwalk_time = datetime.datetime.now()
    
    for x,filepath in enumerate(file_walker.oswalk(walk_dir,verbose)):
        #todo: add progress bar using enumerate somehow
        file_hash = file_hasher.sha512_hasher(filepath) #calculate hash of file
        filename = os.path.basename(filepath) #get filename
        file_hash_dict = {"hash":file_hash,"filename":filename,"filepath":filepath,"hashcompare":True} #create dictionary of file hash details todo add check to hashcompare
        file_hash_dict_list.append(file_hash_dict) #append to list of dictionaries
        vprint(file_hash)

    endwalk_time = datetime.datetime.now()
    
    with open(str(datetime.date.today())+' - '+os.path.basename(walk_dir)+' - file_hash_dict.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ["hash", "filename", "filepath"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        debug_block_heading("Hash table")
        for item in file_hash_dict_list:
            writer.writerow(item)
            vprint(item["hash"],item["filename"])

    endwrite_time = datetime.datetime.now()
    
    spacing = [vprint("") for x in range(5)]
    
    print("file integrity check started at", str(start_date))
    print("file walk took " + str((endwalk_time-startwalk_time).total_seconds()) + " seconds")
    print("file write took " + str((endwrite_time-endwalk_time).total_seconds()) + " seconds")

            
if __name__ == '__main__':
    main()
