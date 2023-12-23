"""
    Basic Cipher Suite

    Basic ciphers to implement password generation.

    Password Ciphers to add
    [X] Viginere Cipher
    [ ] Atbash Cipher
    [ ] ROT13 Cipher
    [ ] Caesar Cipher
    [ ] Affine Cipher
    [ ] Rail-fence Cipher
    [ ] Baconian Cipher
    [ ] Polybius Square Cipher
    [ ] Simple Substitution Cipher
    [ ] Codes and Nomenclators Cipher
    [ ] Columnar Transposition Cipher
    [ ] Autokey Cipher
    [ ] Vigenère and Gronsfeld Cipher
    [ ] Homophonic Substitution Cipher
    [ ] Four-Square Cipher
    [ ] Hill Cipher
    [ ] Playfair Cipher
    [ ] ADFGVX Cipher
    [ ] ADFGX Cipher
    [ ] Bifid Cipher
    [ ] Straddle Checkerboard Cipher
    [ ] Trifid Cipher
    [ ] Base64 Cipher
    [ ] Fractionated Morse Cipher
"""

import numpy

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def Monoalphabetic_Encryption(key,plaintext):
    mono_dict = dict(zip(alphabet,key))
    return [mono_dict[x] for x in plaintext]

def Monoalphabetic_Decryption(key,plaintext):
    mono_dict = dict(zip(key,alphabet))
    return [mono_dict[x] for x in plaintext]

def Row_Transposition_Encryption(key,plaintext):
    pass
    plaintext_array = numpy.array(list(ciphertext)).reshape(int(len(plaintext)/len(key)),len(key))

    print("plaintext array:")
    print(plaintext_array)
    
    inverted_column_order = [key.index(x)+1 for x in range(1,len(key)+1)]
    invert_column_order_0 = [x-1 for x in invert_column_order] #zero indexed

    ciphertext_array = plaintext_array[:,inverted_column_order_0]
    print("ciphertext array:")
    print(ciphertext_array)

    ciphertext_array_1 = ciphertext_array.reshape(1,plaintext_array.size,order='F') #single row
    print("ciphertext:")
    print(ciphertext_array_1)
    return ciphertext_array_1[0]
    
def Row_Transposition_Decryption(key,ciphertext):
    ciphertext_array = numpy.array(list(ciphertext)).reshape(int(len(ciphertext)/len(key)),len(key),order='F')

    print("ciphertext array:")
    print(ciphertext_array)

    key_0 = [x-1 for x in key] #zero indexed
    
    plaintext_array = ciphertext_array[:,key_0]
    print("plaintext array:")
    print(plaintext_array)

    plaintext_array_1 = plaintext_array.reshape(1,plaintext_array.size,order='F') #single row
    print("plaintext:")
    print(plaintext_array_1)
    return plaintext_array_1[0]

    '''dict method
    for j in range(len(K2)):
	for i in range(int(len(ciphertext)/len(K2))):
		rowT[(i,K2[j])]=ciphertext[j+i*len(K2)]
    '''


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


def nCrypt(raw_string, key_word, n=1, decode=False):
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

def main():
    DEBUG_MODE = False
    if DEBUG_MODE:
        secret_message = "That doesn't look like work."
        key = "todd"
        n = 3 
        encoded_message = nCrypt(secret_message, key, n) # This should encode to RoMMCgWcRoUMMYjJGYNYUcaIZ
        print(encoded_message)
        #assert(encoded_message == "HQ:RoMMCgWcRoUMMYjJGYNYUcaIZ")
        
        decoded_message = nCrypt(encoded_message, key, n, decode=True) # This should decode to That doesn't look like work.
        print(decoded_message)
        #assert(decoded_message == "That doesn't look like work.")

    else:    
        option = input("Would you like to encrypt or decrypt a message?: \n1 - encrypt, \n2 - decrypt\n Enter your choice: ")
        if option.lower() in ['quit', 'exit']:
            print('exiting')
            return 

        while option not in ['1','2']:
            option = input("BAD Input please type '1' to encrypt or '2' to decrypt a message?: \n1 - encrypt\n, 2 - decrypt \nEnter your choice: ")
            if option.lower() in ['quit', 'exit']:
                print('exiting')
                return 
        
        decode = option=='1'
        raw_message = input(f"Input a message to {['encrypt', 'decrypt'][int(option)-1]}: ")
        while len(raw_message)==0:
            raw_message = input(f"Bad Input. Please enter a non-empty string. Input a message to {['encrypt', 'decrypt'][int(option)-1]}: ")
            if raw_message in ['quit', 'exit']:
                check = input(f'You entered {raw_message}. Would you like to quit or use that as your message? \n1 - quit \2 - continue')
                if check == '1':
                    print('exiting')
                    return
                else:
                    print(f'Continuing with {raw_message} as your message')


        key = input(f"Input a keyword used to {['encrypt', 'decrypt'][int(option)-1]} the message: ")
        #TODO make this a funciton
        while len(key)==0:
            key = input(f"Bad Input. Please enter a non-empty string. Input a keyword used to {['encrypt', 'decrypt'][int(option)-1]} the message: ")
            if key in ['quit', 'exit']:
                check = input(f'You entered {key}. Would you like to quit or use that as your key? \n1 - quit \2 - continue')
                if check == '1':
                    print('exiting')
                    return
                else:
                    print(f'Continuing with {key} as your keyword')
            
        
        
        # TODO add catch for non int 
        n = input(f"Iterations for {['encryption', 'decryption'][int(option)-1]}: ")
        while not tryMakeInt(n):
            if n.lower() in ['quit', 'exit']:
                print('exiting')
                return 
            n = input(f"Bad input. Input an integer for the number of iterations for {['encryption', 'decryption'][int(option)-1]}: ")
        n = int(n)
            
        result_message = nCrypt(raw_message, key, n, decode)
        print(result_message)
        

if __name__ == '__main__':
    main()