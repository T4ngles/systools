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
    walk_dir = get_dir()
    
    verbose_input = input("Verbose? (Y/N)")
    if verbose_input.upper() == "Y":
        verbose = True
    else:
        verbose = False

    ignore_paths = set([r"c:\Users\rlau0\Documents\Parselmouth\cyberTools\labyrinth"])
    for file in oswalk(walk_dir,verbose,ignore_paths):
        pass #to yield all files in main()
    #walk(walk_dir)
    #globber(walk_dir)

def get_dir():
    print(sys.argv[0])
    walk_dir = os.path.dirname(sys.argv[0]) #walk_dir = walk_dir[0:walk_dir.find(walk_dir.split('/')[-1])]
    walk_dir = input("directory to walk:").replace("\"","")
    return walk_dir

def oswalk(walk_dir,verbose,ignore_paths):
    if verbose:
        def vprint(*args):
            for arg in args:
                print(arg)
    else:
        def vprint(*args):
            pass
        
    vprint("#"*20)    
    vprint("os walk")
    vprint("#"*20)  
    walkedfiles = []

    for roots, folders, files in os.walk(walk_dir):
        folders[:] = [d for d in folders if os.path.join(roots, d) not in ignore_paths]
        folder=''
        for file in files:
            # if any(ele in os.path.split(roots)[0] for ele in ignore_paths):
            #     vprint(f"skippping {os.path.join(roots, file)}")
            # else:
            if folder != os.path.split(roots)[1]:
                folder = os.path.split(roots)[1]
                spacer = 20-len(folder)
                vprint("="*5 + folder + "="*spacer)
            vprint(file)
            yield os.path.join(roots, file)
            
def globber(walk_dir):    
    print("#"*20)  
    print("globber")
    
    for filename in glob.glob(walk_dir + '**/*.txt', recursive=True):
        print(filename)

def stack_exchange_walk(walk_dir):
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
