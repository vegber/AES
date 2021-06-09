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
        var = self.tap_into_matrix(self.plaintext)
        print(var)

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
    key = "secret_kvegardbe" # .encode("utf-8").hex()
    plaintext = "3243f6a8885a308d313198a2e0370734" # .encode("utf-8").hex()
    cipher = Cipher(key, plaintext, 128)

    cipher.Encrypt()
