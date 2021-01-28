from tkinter import *

DEBUG_MODE = False
CHRLIST = [chr(i) for i in range(32,127)]
CHRLIST_MAP = {s:i for i, s in enumerate(CHRLIST)}
M = len(CHRLIST)

def strToIndList(raw_string):
    return [CHRLIST_MAP[s] for s in raw_string]

def _encode(raw_message, key_word):
    """ encode the message using the vignerererre cypher """
    raw_message_int = strToIndList(raw_message)

    repeats = len(raw_message) // len(key_word) + 1
    key_word_int = strToIndList(key_word)
    key_word_int = key_word_int*repeats
    key_word_int = key_word_int[:len(raw_message)] 

    encoded_int = [ (ki + si)%M for ki, si in zip(key_word_int, raw_message_int)]

    return ''.join([CHRLIST[x] for x in encoded_int])


def _decode(encrypted_message, key_word):
    """ decodes the message using the vignerererre cypher """
    
    encrypted_message_int_list = strToIndList(encrypted_message)

    repeats = len(encrypted_message) // len(key_word) + 1
    key_word_int = strToIndList(key_word)
    key_word_int = key_word_int*repeats
    key_word_int = key_word_int[:len(encrypted_message)]
    

    decoded_int = [ (si - ki)%M for ki, si in zip(key_word_int, encrypted_message_int_list)]

    return ''.join([CHRLIST[x] for x in decoded_int])


def show_entry_fields():
    print(f"Message is {e1.get()} and Keyword is {e2.get()}")

master = Tk()
Label(master, text="Message").grid(row=0)
Label(master, text="Key word").grid(row=1)
Label(master, text="Output").grid(row=2)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e1.insert(0,"secret")
e2.insert(0,"key")
e3.insert(0,"output")

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

Button(master, text="Quit", command=master.quit).grid(row=3, column=2, sticky=W, pady=4)
Button(master, text="Encode", command=e3.insert(0,str(_encode(e1.get(),e2.get())))).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text="Decode", command=e3.insert(0,str(_decode(e1.get(),e2.get())))).grid(row=3, column=1, sticky=W, pady=4)

mainloop()
