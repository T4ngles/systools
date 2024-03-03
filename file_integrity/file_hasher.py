"""
    File hasher for integrity check
    to add:
        -different hashing methods
        -lower level file data access
"""

import hashlib
import sys
import os

def string_md5_hasher(plaintext):
    hashlib.md5().update(str(plaintext).encode("utf-8","replace"))
    return hashlib.md5().hexdigest()

def md5_hasher(filepath):
    return hashlib.md5(open(filepath,'rb').read()).hexdigest()

def sha256_hasher(filepath):
    return hashlib.sha256(open(filepath,'rb').read()).hexdigest()

def sha256_hasher_string(strInput):
    return hashlib.sha256(strInput.encode('utf-8')).hexdigest()

def sha512_hasher(filepath):
    return hashlib.sha512(open(filepath,'rb').read()).hexdigest()
 
def file_hash(filepath,hash_type):
    try:
        if hash_type == "md5":
            hash_out = md5_hasher(filepath)
        if hash_type == "sha256":
            hash_out = sha256_hasher(filepath)
        if hash_type == "sha512":
            hash_out = sha512_hasher(filepath)            
    except PermissionError:
        hash_out = "Permission ERROR" + filepath
    except OSError:
        hash_out = "OS ERROR" + filepath
    except MemoryError:
        hash_out = "MemoryError" + filepath

    filename = filepath.split(sep='\\')[-1]
    #print(hash_out,':',filename)
    
    return hash_out


def user_file_hash(hash_type):
    filepath = input("filepath:").replace("\"","")
    print("filepath:",filepath)
    filename = filepath.split(sep='\\')[-1]
    print('='*len(filename))
    print(filename)
    print('='*len(filename))
    hash_out = ""

    try:
        hash_out = file_hash(filepath,hash_type)      
    except PermissionError:
        hash_out = "Permission ERROR"
    except OSError:
        hash_out = "OS ERROR"
    except MemoryError:
        hash_out = "MemoryError"

    print(hash_type,':',hash_out)
    
    return hash_out

def main():

    hash_choice = {
        "1": "md5",
        "2": "sha256",
        "3": "sha512",
    }

    for k,v in hash_choice.items():
        print(k, ":", v)

    hash_type = hash_choice[input("choose hash type:")]
    print(f"using {hash_type}")

    user_file_hash(hash_type)
    
if __name__ == '__main__':
    main()
    

#C:\Users\rlau0\Downloads\stegano1.bmp

