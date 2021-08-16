"""
    Filewalker:
        -lists all files and folders below a folder directory
        -lists all files in a drive
        -provides a % value of each folder in each folder level
"""

import os
import sys
import glob

def main():
    print(sys.argv[0])
    walk_dir = os.path.dirname(sys.argv[0])
    #walk_dir = walk_dir[0:walk_dir.find(walk_dir.split('/')[-1])]
    raywalk(walk_dir)
    #walk(walk_dir)
    #globber(walk_dir)


def raywalk(walk_dir):
    print("#"*20)    
    print("raywalk")    

    for root, subFolders, files in os.walk(walk_dir):

        for file in files:
            print("- " + file)
                
        for folder in subFolders:
            spacer = 20-len(folder)
            print("="*5 + folder + "="*spacer)

            for file in files:
                print("- " + file)

def globber(walk_dir):    
    print("#"*20)  
    print("globber")
    
    for filename in glob.glob(walk_dir + '**/*.txt', recursive=True):
        print(filename)

def walk(walk_dir):
    print("#"*20)
    print("walk")
    
    print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

    for root, subdirs, files in os.walk(walk_dir):
        print('--\nroot = ' + root)
        list_file_path = os.path.join(root, 'my-directory-list.txt')
        print('list_file_path = ' + list_file_path)

        with open(list_file_path, 'wb') as list_file:
            for subdir in subdirs:
                print('\t- subdirectory ' + subdir)

            for filename in files:
                file_path = os.path.join(root, filename)

                print('\t- file %s (full path: %s)' % (filename, file_path))

                with open(file_path, 'rb') as f:
                    f_content = f.read()
                    list_file.write(('The file %s contains:\n' % filename).encode('utf-8'))
                    list_file.write(f_content)
                    list_file.write(b'\n')

if __name__ == "__main__":
    main()
