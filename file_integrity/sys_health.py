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

import sys
import os
import file_walker
import file_hasher
import csv
import datetime
import glob
import time


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

    walk_dir = os.path.splitdrive(sys.argv[0])[0] + "\\"#C drive 
    hash_type = "sha256"
    print(hash_type + " File Integrity Check of " + walk_dir)

    ignore_path = os.path.dirname(sys.argv[0]) + "\\pathsToIgnore.txt"
    with open(ignore_path, "r") as ignore_path_file:
        paths_to_ignore = set([line.strip() for line in ignore_path_file.readlines()])
    
    print(f"ignoring paths in {paths_to_ignore}")

    startwalk_time = datetime.datetime.now()

    #split off threads to scan multiple jobs in C drive. One per folder and one for files in C drive. output is seperate or can all append to the one(three) log file(s).
    cDirectories = [y for y in os.listdir("C:\\") if os.path.isdir("C:\\"+y)]
    cFiles = [y for y in os.listdir("C:\\") if os.path.isfile("C:\\"+y)]

    #BREAK OFF LOG LOADING
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
    duplicate_files = {} #create dictionary to store duplicate file entries

    if latest_log != "":
        
        print('...loading latest hash log file')
        #open old hashlist csv and check current hashes with hashes in csv
        old_hash_set = set()
        oldLogSize = 0
        with open(latest_log, 'r', encoding='utf-8', newline='') as readcsvfile:
            reader = csv.DictReader(readcsvfile)
            for item in reader:
                file_key = item["hash"]+file_hasher.sha256_hasher_string(item["filepath"])
                old_hash_set.add(file_key)
                oldLogSize = oldLogSize + 1
     
    print(f"{oldLogSize} files exist in old log")

    #BREAK OFF HASHWALK TO ALLOW THREADING OF MULTIPLE JOBS
    #Main hash walk
    #walk through files and compute hashes and add to dictionary of hashes
    print('...hash walking the current files')
    file_hash_dict_dict = {} 
    walked_hashes_set = set()
    new_files_containers = {}

    for x,filepath in enumerate(file_walker.oswalk(walk_dir,verbose = False, ignore_paths = paths_to_ignore)):
        #todo: add progress bar using enumerate somehow
        percStr = str(round((x+1)/oldLogSize*100,0))
        progress = (3-len(percStr))*" " + percStr + "%"

        file_hash = file_hasher.file_hash(filepath,hash_type) #calculate hash of file        
        filename = os.path.basename(filepath).replace(",", " ") #get filename and replace commas with spaces

        #need to have hash of filepath? for unique key just use file_hash+filepath
        #file ident cases:
        #same file in multiple locations
        #same file in same location different name
        filepath_hash = file_hasher.sha256_hasher_string(filepath) #calculate hash of filepath

        file_key = file_hash+filepath_hash
        
        #check if hash is already found in walk
        #hash found already in walk
        #TODO: THIS CHECKS IF HASH ALREADY IN WALK BUT MISSES OUT ON FILEPATH OF INITIAL HASH FIND
        if file_hash in walked_hashes_set:
            vprint("===hash already found===")
            filesize = os.path.getsize(filepath)/(1024 * 1024)
            duplicate_files[file_key] = {"filename":filename,"filepath":filepath, "hash":file_hash, "filesize":filesize}
        #hash not found in walk yet
        else:
            walked_hashes_set.add(file_hash)    #add hash to hash set 

        #compare hash to latest log hash todo change this to hashes set.
        if old_hash_set:
            if file_key in old_hash_set:  #hash found in previous log
                hashfound = True
            else:   #hash isn't in previous log so is new file or has changed
                hashfound = False
                new_files[file_key] = {"filename":filename,"filepath":filepath}
                file_folder = os.path.split(filepath)[0]
                try:
                    if new_files_containers[file_folder]:
                        new_files_containers[file_folder] = new_files_containers[file_folder] + 1
                except  KeyError:
                    new_files_containers[file_folder] = 1
                    

        file_hash_dict = {"hash":file_hash,"filename":filename,"filepath":filepath,"hashfound":hashfound} #create dictionary of file hash details                         
        file_hash_dict_dict[file_key] = file_hash_dict #add file hash dictionary to upper dictionary using walk_id and file hash as the key

        vprint(int(hashfound), " ", file_hash, ":", len(file_hash_dict_dict), "/", filename, " at ", filepath)

        if not verbose:
            print(" | ".join([str(x) for x in [progress, (x+1), len(new_files), len(duplicate_files), filepath, filename[0:60], 8*"   "]]), end="\r")
            
    endwalk_time = datetime.datetime.now()

    print_space()
    print("HASH WALK log write")
    
    log_name = logs_path + str(datetime.datetime.now().strftime("%d-%m-%Y %H%M%S"))+' - '+os.path.basename(walk_dir)+' - file_hash_dict.csv'     
    
    #BREAK OFF LOG WRITING
    #Main log
    with open(log_name, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ["hash", "filepath"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for file_hash in file_hash_dict_dict.values():
            filtered_row = {key: value for key, value in file_hash.items() if key in fieldnames}
            writer.writerow(filtered_row) 

    endwrite_time = datetime.datetime.now()
    
    print("log file saved at " + log_name)    
    print_space()

    #New files Log
    print("NEW FILES")
    if new_files:
        new_files_Number = str(len(new_files))
        print( new_files_Number + " new files or modifications found")
        for item in new_files.values():
            vprint(item["filename"] + "    " + item["filepath"])
        #write out new hash file for inspection
        new_files_log_name = logs_path + str(datetime.datetime.now().strftime("%d-%m-%Y %H%M%S"))+' - '+os.path.basename(walk_dir)+' - new_files.txt'
        with open(new_files_log_name, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ["filepath"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for file_hash in new_files.values():
                filtered_row = {key: value for key, value in file_hash.items() if key in fieldnames}
                writer.writerow(filtered_row) 
        
        print("new files hash csv log saved at ", new_files_log_name)
        print("Summary of New files:")
        print(f"There are {len(new_files_containers)} containers of new files")
        for fileContainer in sorted(new_files_containers.items(), key=lambda x: x[1]):
            print(fileContainer) #tuple of filepath and number of files. Add a sum of filesize as well?
        print_space()
        
    else:
        print("no new files or modifications found")
        new_files_Number = 0
    
    #Duplicate File Log
    print("DUPLICATE FILES")
    if duplicate_files:
        dup_files_Number = str(len(duplicate_files))
        print( dup_files_Number + " duplicate files found")
        for item in duplicate_files.values():
            vprint("    ".join([str(x) for x in [item["filename"],item["filepath"],item["hash"],item["filesize"]]]))
        #write out duplicate hash file for inspection
        # dup_files_log_name = logs_path + str(datetime.datetime.now().strftime("%d-%m-%Y %H%M%S"))+' - '+os.path.basename(walk_dir)+' - dup_files.txt'
        # with open(dup_files_log_name, 'w', encoding='utf-8', newline='') as csvfile:
        #     fieldnames = ["filepath","hash","filesize"]
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     writer.writeheader()
        #     for file_hash in duplicate_files.values():
        #         filtered_row = {key: value for key, value in file_hash.items() if key in fieldnames}
        #         writer.writerow(filtered_row) 
        
        # print("dupilcate files hash csv log saved at ", dup_files_log_name)
        print_space()

    else:
        print("no duplicates found")
        dup_files_Number = 0
    
    print_space()

    print(f"file walk of {str(len(file_hash_dict_dict))} files ({new_files_Number} new) took {((endwalk_time-startwalk_time).total_seconds()/60):.2f} minutes")
    print(f"log comparison and write took {((endwrite_time-endwalk_time).total_seconds()/60):.2f} minutes")

            
if __name__ == '__main__':
    main()
