"""
ECB - Electronic Code Book mode AES
"""
import sys
import os
sys.path.append(os.getcwd())
from AES import Cipher
from DataManagement import *

"""Given memory limit, I will not have a constructor
due to the fact that I want to support big data.
"""

def encrypt_by_terminal():
    password, text = get_io("Encryption")
    key_frase = ''.join(password)
    for x in range(len(text)):
        aes = Cipher(key_frase, ''.join(text[x]), 128)
        aes.Encrypt()
        aes.printable(False)

def get_io(mode):
    print()
    print(f"You are now in {mode} mode\nPlease enter "
          f"the following: ")
    print()
    while True:
        password = input(f"{mode} Key: ")
        if len(password) > 16:
            print("Key cannot be longer than 128 bits, or 16 ASCII chars! ")
        else:
            break
    # password = input(f"{mode} Key: ")
    choice = input("Text as HEX or ASCII, default ASCII (Y/n): ")
    if not choice:
        text = ascii_to_hex(input(f"{mode} Text: "))
    else:
        text = (input(f"{mode} Text: ")).replace(' ', '')
    return stream_to_blocks(ascii_to_hex(password)), stream_to_blocks(text)

def decrypt_by_terminal():
    password, text = get_io("Decryption")
    key_frase = ''.join(password)
    plaintext = ""
    for x in range(len(text)):
        aes = Cipher(key_frase, ''.join(text[x]), 128)
        aes.Decrypt()
        out = aes.get_state()
        stringed_out = two_by_two_to_str(out)
        plaintext += (hex_to_ascii(stringed_out))
    print(plaintext)

        #aes.printable(False)

def encrypt_file_read(filename, outfile):
    pass

def read_from_file(file_name):
    with open(file_name, "r+") as file:
        return file.readlines()

def decrypt_file_read(self, cipherfile, plainfile):
    pass

if __name__ == '__main__':
    encrypt_by_terminal()
    decrypt_by_terminal()
