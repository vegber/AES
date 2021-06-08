

class Cipher:

    def __init__(self, key, plaintext):
        self.key = key # Key is n bits
        self.plaintext = plaintext
        pass


    def Encrypt(self):
        print(self.plaintext)




if __name__ == '__main__':

    cipher = Cipher("HelloWorld", "Plaintext")
    cipher.Encrypt()