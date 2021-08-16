"""
    File hasher for integrity check
    to add:
        -recursive loop for all directories and files below target
        -store of hash result in dictionary
        -encryption of hash result
"""

import hashlib
import os
import glob

def str_hasher(filepath):    
    with open(filepath) as f:
        lines = f.readlines()
    for line in lines:
        hashlib.md5().update(line.encode('utf-8'))
    return hashlib.md5().hexdigest()

def general_hasher(filepath):
    return hashlib.md5(open(filepath,'rb').read()).hexdigest()    

if __name__ == '__main__':
    filepath = input("filepath:")
    filename = filepath.split(sep='\\')[-1]
    print('='*len(filename))
    print(filename)
    print('='*len(filename))
    try:
        print('string hash:',str_hasher(filepath))
    except UnicodeDecodeError:
        print('general hash:',general_hasher(filepath))

#C:\Users\rlau0\Downloads\stegano1.bmp
#C:\Users\rlau0\Downloads\Mr.Robot.S04E04.iNTERNAL.480p.x264-mSD[eztv].mkv