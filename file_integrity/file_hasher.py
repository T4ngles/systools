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
    try:
        hash = hashlib.sha512(open(filepath,'rb').read()).hexdigest()
    except PermissionError:
        hash = "Permission ERROR"
    except OSError:
        hash = "OS ERROR"
    return hash
 
def file_hash():
    filepath = input("filepath:").replace("\"","")
    print("filepath:",filepath)
    filename = filepath.split(sep='\\')[-1]
    print('='*len(filename))
    print(filename)
    print('='*len(filename))
    print('sha512 hash:',sha512_hasher(filepath))

def main():
    
    file_hash()
    
if __name__ == '__main__':
    main()
    

#C:\Users\rlau0\Downloads\stegano1.bmp

