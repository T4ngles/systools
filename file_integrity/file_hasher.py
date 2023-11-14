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
    print(filename,':',hash_out)
    
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
    return hash_out

    print(hash_type,':',hash_out)

def main():
    
    user_file_hash("sha256")
    
if __name__ == '__main__':
    main()
    

#C:\Users\rlau0\Downloads\stegano1.bmp

