"""
    String Exporter
    to add:
        -
        
"""

import os
import file_walker

def main():
        string = input("String to export:")
        string = string.replace("\n"," ")        
        dirpath = r"C:\Users\rlau0\Downloads\CSU ITC595 Lectures"
        files = []
        for file in file_walker.raywalk(dirpath,True):
                files.append(os.path.basename(file))
        filename = input("filename:")
        while filename + ".txt" in files:
                print("filename already exists. Choose new name.")
                filename = input("filename:")                
        filepath = os.path.join(dirpath,filename+".txt")
        with open(filepath,"w") as f:
                f.write(string)
                f.close()

if __name__ == '__main__':
    main()
