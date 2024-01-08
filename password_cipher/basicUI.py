"""
    Basic Password Tester/Cipher/Encrypter GUI

    To test strength of passwords using backend scripts and to generate and 
    store passwords using personal keys. Demonstration of password strength,
    ciphers, and encryption standards

    [ ]amalgamate script files into one backend import script
    [X]create window with basic encrypt decrypt functions

    Password Testing
    [ ]basic password hygiene discrete tests (NIST,ASD)
    [ ]Replicate hashcat/JTR brute force code to test passwords

    Password Storage and Encryption
    [ ]import saved passwords on startup
    [ ]export saved passwords on save button 
    [ ]encrypt/decrypt password file using public/private key
"""

import tkinter as tk
from datetime import datetime

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

def _nCipher(raw_string, key_word, n=1, decode=False):
    """ encrypts n times
        if decode flag is true, decodes an encrypted message
    """
    result = raw_string
    if not decode:    
        for _ in range(n):
            result = _encode(result, key_word)
    
    else:
        for _ in range(n):
            result = _decode(result, key_word)

    return result

def tryMakeInt(string):
    try:
        int(string)
        return True
    except:
        return False

class userWindow:

    def __init__(self):

        self.master = tk.Tk()

        self.master.title("Password Cipher")

        self.label1 = tk.Label(self.master, text="Message").grid(row=0)
        self.label2 = tk.Label(self.master, text="Key word").grid(row=1)
        self.label3 = tk.Label(self.master, text="Output").grid(row=2)
        
        self.label4 = tk.Label(self.master, text="Password Tester").grid(row=4)
        self.label6 = tk.Label(self.master, text="Number of Times").grid(row=6)

        self.e1 = tk.Entry(self.master)
        self.e2 = tk.Entry(self.master)
        self.e3 = tk.Entry(self.master)
        self.e6 = tk.Entry(self.master)

        self.e1.insert(0,"secret")
        self.e2.insert(0,"key")        
        self.e6.insert(0,"88")

        self.e3.insert(0,"output")

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e6.grid(row=6, column=1)
        

        buttonframe = tk.Frame(self.master)
        buttonframe.columnconfigure(0, weight=1)
        buttonframe.columnconfigure(1, weight=1)
        buttonframe.columnconfigure(2, weight=1)

        self.b1 = tk.Button(self.master, text="Encode", command=self._encodeButton).grid(row=3, column=0, sticky=tk.W, pady=4)
        self.b2 = tk.Button(self.master, text="Decode", command=self._decodeButton).grid(row=3, column=1, sticky=tk.W, pady=4)
        self.b3 = tk.Button(self.master, text="Quit", command=self.master.quit).grid(row=3, column=2, sticky=tk.W+tk.E, pady=4)


        self.e4 = tk.Entry(self.master)
        self.e5 = tk.Entry(self.master)
        self.e4.insert(0,"Password")
        self.e5.insert(0,"test")


        self.e4.grid(row=4, column=1)
        self.e5.grid(row=5, column=1)

        self.b4 = tk.Button(self.master, text="Test", command=self._passwordTest).grid(row=5, column=0, sticky=tk.W, pady=4)

        self.master.mainloop()
    
    def _encodeButton(self):
        self.e3.delete(0, tk.END)

        message = self.e1.get()
        key = self.e2.get()
        reps = int(self.e6.get())
        output = str(_nCipher(message,key,reps,False))
        
        self.e3.insert(0,output)

        self.e5.delete(0, tk.END)
        self.e5.insert(0,output)
        
        print(f"encoded {reps} times")
    
    def _decodeButton(self):    
        self.e3.delete(0, tk.END)

        message = self.e1.get()
        key = self.e2.get()
        reps = int(self.e6.get())
        output = str(_nCipher(message,key,reps,True))
        
        self.e3.insert(0,output)

        self.e5.delete(0, tk.END)
        self.e5.insert(0,output)
        
        print(f"decoded {reps} times")

    def show_entry_fields(self):
        print(f"Message is {self.e1.get()} and Keyword is {self.e2.get()}")

    def _passwordTest(self):
        passwordString = self.e5.get()
        print(passwordString)
        self.show_entry_fields()

#=========MAIN Function=============
        
if __name__ == "__main__":
    print ('It is currently:' + str(datetime.now().time()))
    window = userWindow()