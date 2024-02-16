"""
    System health check
    to add: (* denotes in progress)
        File Backup
        System component health check
        System Internal traffic monitor
        System External traffic monitor
        [X]File integrity (Start up and Shutdown scheduled check)
            [X]include progress bar of walk through files            
            [ ]include comparison to malware hash database
            [X]read in most recent log for comparison
            [ ]append to log with summary of file changes and additions
            [ ]create a sqlite database to serve the file hashes
            [ ]include Virus Total API for file hash inspection*
            [ ]include CYB3RMX MalwareHashDB for file md5 hash comparison

            [ ]improve walk speed
            [ ]encryption and decrption of file hash csv            
            [ ]visualisation of changes
            [ ]incorporate fuzzy hashing or context triggered piecewise hashes
            
           
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
            finalArg = ""
            for arg in args:
                finalArg = finalArg + str(arg)
            print(finalArg)
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
        spacing = [print("") for x in range(1)]
        print(20*"-")

    #os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0])))) #Documents folder #os.path.dirname(sys.argv[0]) #file_integrity folder
    #walk_dir = os.path.dirname(sys.argv[0]) #file_integrity folder
    walk_dir = os.path.splitdrive(sys.argv[0])[0] + "\\"#C drive 
    walk_dir = "c:\\"
    hash_type = "sha256"
    print(hash_type + " File Integrity Check of " + walk_dir)
    startwalk_time = datetime.datetime.now()

    #Load in latest log of hashes
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
        os.mkdir(logs_path)   #todo fix this need to actually create an empty log file? 

    new_files = {} #create dictionary to store new file entries

    if latest_log != "":
        
        print('...loading latest hash log file')
        #open old hashlist csv and check current hashes with hashes in csv
        old_hash_dict = {}
        with open(latest_log, 'r', encoding='utf-8', newline='') as readcsvfile:
            reader = csv.DictReader(readcsvfile)
            for item in reader:
                old_hash_dict[item["hash"]] = item

    oldLogSize = len(old_hash_dict)

    #Main hash walk
    #walk through files and compute hashes and add to dictionary of hashes
    print('...hash walking the current files')
    file_hash_dict_dict = {} 

    for x,filepath in enumerate(file_walker.oswalk(walk_dir,verbose = False)):
        #todo: add progress bar using enumerate somehow
        progress = str(x) + (6-len(str(x)))*" " + f"/ {oldLogSize} files walked"
        percStr = str(round(x/oldLogSize*100,0))
        progress = (3-len(percStr))*" " + percStr + "%"
        if not verbose:
            print(progress, end="\r")
        file_hash = file_hasher.file_hash(filepath,hash_type) #calculate hash of file
        filename = os.path.basename(filepath) #get filename

        #compare hash
        if old_hash_dict:
            if file_hash in old_hash_dict:
                hashfound = True
            else:
                hashfound = False
                new_files[file_hash] = file_hash_dict = {"hash":file_hash,"filename":filename,"filepath":filepath,"hashfound":hashfound}

        file_hash_dict = {"hash":file_hash,"filename":filename,"filepath":filepath,"hashfound":hashfound} #create dictionary of file hash details 
        file_hash_dict_dict[file_hash] = file_hash_dict
        vprint(int(hashfound), " ", file_hash, ":", filename)

    endwalk_time = datetime.datetime.now()

    print_space()

    
    log_name = logs_path + str(datetime.datetime.now().strftime("%d-%m-%Y %H%M%S"))+' - '+os.path.basename(walk_dir)+' - file_hash_dict.csv'     
    
    with open(log_name, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ["hash", "filename", "filepath", "hashfound"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for file_hash in file_hash_dict_dict.values():
            writer.writerow(file_hash)

    endwrite_time = datetime.datetime.now()
    print_space()
    
    print("log file saved at " + log_name)

    if new_files:
        new_files_Number = str(len(new_files))
        print( new_files_Number + " new files or modifications found:")
        for item in new_files.values():
            vprint(item["filename"] + "    " + item["filepath"])
        #write out new hash file for inspection
        new_files_log_name = logs_path + str(datetime.datetime.now().strftime("%d-%m-%Y %H%M%S"))+' - '+os.path.basename(walk_dir)+' - new_files.txt'
        with open(new_files_log_name, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ["filename", "filepath"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for file_hash in new_files.values():
                filtered_row = {key: value for key, value in file_hash.items() if key in fieldnames}
                writer.writerow(filtered_row) 
        print_space()
        print("new files hash csv log saved at ", new_files_log_name)

    else:
        print("no new files or modifications found")
    
    print_space()

    print(f"file walk of {str(len(file_hash_dict_dict))} files ({new_files_Number} new) took {str((endwalk_time-startwalk_time).total_seconds())} seconds")
    print("log comparison and write took " + str((endwrite_time-endwalk_time).total_seconds()) + " seconds")

    print_space()


    

            
if __name__ == '__main__':
    main()
