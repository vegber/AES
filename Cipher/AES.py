class Cipher:
    round_keys = []
    state = []

    def __init__(self, key, plaintext, key_size):
        self.key = key  # Key is n bits
        self.plaintext = plaintext
        self.key_size = key_size

    def Encrypt(self):
        # Call upon keygen
        self.round_keys, rounds = self.keyGeneration(self.key, self.key_size)
        # turn plaintext to "matrix"
        self.tap_into_matrix(self.plaintext)

        for x in range(rounds): # n -1 rounds
            self.subbytes(self.state)
            self.shift_rows(self.state)
            self.mix_columns(self.state)
            self.add_round_key(self.state)
            # Now last round
        self.subbytes(self.state)
        self.shift_rows(self.state)
        self.add_round_key(self.state)

        return self.state

    def keyGeneration(self, key, key_size):
        keylist = []
        if key_size == 128:
            return keylist, 9
        if key_size == 196:
            return keylist, 11
        if key_size == 256:
            return keylist, 13

    def subbytes(self, state):
        pass

    def shift_rows(self, state):
        pass

    def mix_columns(self, state):
        pass

    def add_round_key(self, state):
        pass

    def tap_into_matrix(self, content):
        matrix = []
        for iter in range(16):
            pass


if __name__ == '__main__':
    key = "secret_kvegardbe".encode("utf-8").hex()
    plaintext = "00000101030307070f0f1f1f3f3f7f7f".encode("utf-8").hex()
    print(plaintext)
    cipher = Cipher(key, plaintext, 128)

    cipher.Encrypt()
