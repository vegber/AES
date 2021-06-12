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
    password = get_key(mode)
    # password = input(f"{mode} Key: ")
    choice = input("Text as HEX or ASCII, default ASCII (Y/n): ")
    if not choice:
        text = ascii_to_hex(input(f"{mode} Text: "))
    else:
        text = (input(f"{mode} Text: ")).replace(' ', '')
    return stream_to_blocks(ascii_to_hex(password)), stream_to_blocks(text)


def get_key(mode):
    while True:
        password = input(f"{mode} Key: ")
        if len(password) > 16:
            print("Key cannot be longer than 128 bits, or 16 ASCII chars! ")
        else:
            break
    return password


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

def encrypt_file_read(filename, outfile, reading_mode, key):
    """
    This method is going read plaintext from a file.
        - We are going need to know weather the file is written
        in *HEX or *ASCII (reading_mode)
        - read content of file.
        - block the content of the file in 128 bit segments
        - iterate over AES cipher with blocks
        - writing the output instantly to preserve memory use
    close()
    :param filename:
    :param outfile:
    :return:
    """
    opened_file = read_from_file(filename)
    formatted_content = format_content(opened_file, reading_mode)
    password = ascii_to_hex(''.join(key))
    out = ""
    for x in range(len(formatted_content)):
        aes = Cipher(password, ''.join(formatted_content[x]), 128)
        aes.Encrypt()
        enc_round = two_by_two_to_str(aes.get_state())
        out += enc_round
    write_to_file(out, outfile)

def read_from_file(file_name):
    with open(file_name, "r+") as file:
        return file.readlines()

def decrypt_file_read(cipherfile, plainfile):
    pass


def format():
    global file_format
    if not file_format:
        file_format = True
    else:
        file_format = False


if __name__ == '__main__':
    while True:
        choice = input("Welcome to AES in ECB mode.\nWhich mode do you want: \n"
                       "\tEncrypt via Terminal (1)\n"
                       "\tDecrypt via Terminal (2)\n"
                       "\tEncrypt file to file (3)\n"
                       "\tDecrypt file to file (4)\n"
                       ""
                       "I want to: ")
        if choice == '1':
            encrypt_by_terminal()
            break
        elif choice == '2':
            decrypt_by_terminal()
            break
        elif choice == '3':

            file_format = input("Is the file in:  (default) ASCII / hex (Y/n)")
            format()
            key = get_key("Encryption")
            file1 = input("Plaintext file: (with file extension) ")
            outfile = input("Out file: (with file extension) ")
            encrypt_file_read(file1, outfile, file_format, key)
            break
        elif choice == '4':
            file1 = input("Cipher file: (with file extension) ")
            outfile = input("Out file: (with file extension) ")
            decrypt_file_read(file1, outfile)
            break
        print("Sorry, did not understand that! \n\t")


