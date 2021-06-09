class Cipher:
    keys = []
    state = []
    rounds = 0
    def __init__(self, key, plaintext, key_size):
        self.key = key  # Key is n bits
        self.plaintext = plaintext
        self.key_size = key_size
        self.round_keys(key, key_size)

    def Encrypt(self):
        # Call upon keygen
        # turn plaintext to "matrix"
        self.state = self.tap_into_matrix(self.plaintext)
        self.add_round_key(self.state, self.keys)

        for x in range(self.rounds): # n -1 rounds
            self.subbytes(self.state)
            self.shift_rows(self.state)
            self.mix_columns(self.state)
            self.add_round_key(self.state, self.keys)
            # Now last round
        self.subbytes(self.state)
        self.shift_rows(self.state)
        self.add_round_key(self.state, self.keys)

        return self.state

    def round_keys(self, key, key_size):
        #TODO
        # key to matrix form
        # generate all the round keys
        # update the keys[] list
        key_matrix = self.tap_into_matrix(key)
        print(key_matrix)
        keylist = []
        if key_size == 128:
            return keylist, 9
        if key_size == 196:
            return keylist, 11
        if key_size == 256:
            return keylist, 13

    def subbytes(self, state):
        #TODO
        pass

    def shift_rows(self, state):
        #TODO
        pass

    def mix_columns(self, state):
        #TODO
        pass

    def add_round_key(self, state, key_round):
        for i in range(4):
            for j in range(4):
                state[i][j] ^= key_round[i][j]

    def tap_into_matrix(self, content):
        shaped_array, state = self.sort_array_to_matrix_state(content)
        for x in range(4):
            for i in range(len(state)):
                if i % 4 == x:
                    shaped_array.append(state[i])
        matrix = [[x for x in shaped_array[i:i+4]] for i in range(0, len(shaped_array), 4)]
        return matrix

    def sort_array_to_matrix_state(self, content):
        s = " ".join(content[i:i + 2] for i in range(0, len(content), 2))
        state = [x for x in s.split()]
        shaped_array = []
        # sorted array
        return shaped_array, state


if __name__ == '__main__':

    # dont need to convert this, since already hex
    key = "2b7e151628aed2a6abf7158809cf4f3c" # .encode("utf-8").hex()
    plaintext = "3243f6a8885a308d313198a2e0370734" # .encode("utf-8").hex()
    cipher = Cipher(key, plaintext, 128)

    cipher.Encrypt()
