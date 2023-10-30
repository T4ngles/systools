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
            -length comparison of dictionary to current files
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
import glob

def main():
    
    start_date = datetime.datetime.now()
    print("#"*200)
    print("File integrity check started at", str(start_date))
    
    verbose = False

    if verbose:
        def vprint(*args):
            for arg in args:
                print(arg)
    else:
        def vprint(*args):
            pass

    def debug_block_heading(title):
        title_length = len(title)
        block_size = 100
        spacer = "="*int((block_size-title_length)/2)
        spacer_length = len(spacer)+1
        leftover = block_size-2*spacer_length-title_length
        vprint("")
        vprint("="*block_size)
        vprint(spacer+title+spacer+"="*leftover)
        vprint("="*block_size)
        vprint("")

    def print_space():
        spacing = [print("") for x in range(2)]

    #os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0])))) #Documents folder #os.path.dirname(sys.argv[0]) #file_integrity folder
    #walk_dir = os.path.dirname(sys.argv[0]) #file_integrity folder
    walk_dir = os.path.splitdrive(sys.argv[0])[0] + "\\"#C drive 
    walk_dir = "c:\\"
    hash_type = "sha512"
    print(hash_type + " File Integrity Check of " + walk_dir)
    startwalk_time = datetime.datetime.now()

    #walk through files and compute hashes and add to dictionary of hashes
    file_hash_dict_dict = {} 
    for x,filepath in enumerate(file_walker.oswalk(walk_dir,verbose)):
        #todo: add progress bar using enumerate somehow
        file_hash = file_hasher.file_hash(filepath,hash_type) #calculate hash of file
        filename = os.path.basename(filepath) #get filename
        file_hash_dict = {"hash":file_hash,"filename":filename,"filepath":filepath,"hashfound":False} #create dictionary of file hash details 
        file_hash_dict_dict[file_hash] = file_hash_dict

    endwalk_time = datetime.datetime.now()

    print_space()
    print("file walk of " + str(len(file_hash_dict_dict)) + " files took " + str((endwalk_time-startwalk_time).total_seconds()) + " seconds")

    #get latest log file
    logs_path = os.path.dirname(sys.argv[0]) + "\\logs\\"
    file_type = r'\*csv'
    files = glob.glob(logs_path + file_type)
    latest_log = ""
    try:
        latest_log = max(files, key=os.path.getctime)
        print_space()
        print("latest log found at " + latest_log)
    except ValueError:
        print("No Logs found. Creating log")
        os.mkdir(logs_path)    

    fieldnames = ["hash", "filename", "filepath", "hashfound"]

    if latest_log != "":
        #open old hashlist csv and check current hashes with hashes in csv
        old_hash_dict = {}
        new_files = {}

        with open(latest_log, 'r', encoding='utf-8', newline='') as readcsvfile:
            reader = csv.DictReader(readcsvfile)
            for item in reader:
                old_hash_dict[item["hash"]] = item

    #compare new hashlist to old and write out new hash summary log
    log_name = logs_path + str(datetime.datetime.now().strftime("%d-%m-%Y %H%M%S"))+' - '+os.path.basename(walk_dir)+' - file_hash_dict.csv'     
    
    with open(log_name, 'w', encoding='utf-8', newline='') as csvfile:
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        debug_block_heading("Hash table")

        for file_hash in file_hash_dict_dict.values():

            if latest_log != "":
                if file_hash["hash"] in old_hash_dict:
                    file_hash["hashfound"] = True
                else:
                    file_hash["hashfound"] = False
                    new_files[file_hash["hash"]] = file_hash

            writer.writerow(file_hash)
            vprint(file_hash["hash"] + "    " + file_hash["filename"])

    endwrite_time = datetime.datetime.now()

    if new_files:
        print("new files or modifications found for the following files:")
        for item in new_files.values():
            print(item["filename"] + "    " + item["filepath"])
    else:
        print("no new files or modifications found")
    
    print_space()

    print("file walk of " + str(len(file_hash_dict_dict)) + " files took " + str((endwalk_time-startwalk_time).total_seconds()) + " seconds")
    print("log comparison and write took " + str((endwrite_time-endwalk_time).total_seconds()) + " seconds")
    print("log file saved at " + log_name)

    print_space()

    

            
if __name__ == '__main__':
    main()
