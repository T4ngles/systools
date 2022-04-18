"""
    Basic Cipher Suite
    /tgcid/
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
