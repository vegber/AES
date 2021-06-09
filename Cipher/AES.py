from BitVector import *

from static.S_BOX import M_aes


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
        for x in range(self.rounds):  # n -1 rounds
            self.round_encyption()
            # Now last round
        self.last_round()
        return self.state

    def last_round(self):
        self.subbytes(self.state)
        self.shift_rows(self.state)
        self.add_round_key(self.state, self.keys)

    def round_encyption(self):
        self.subbytes(self.state)
        self.shift_rows(self.state)
        self.mix_columns(self.state)
        self.add_round_key(self.state, self.keys)

    def round_keys(self, key, key_size):
        # TODO
        # key to matrix form
        # generate all the round keys
        # update the keys[] list
        self.keys.append(self.tap_into_matrix(key))
        keylist = []
        if key_size == 128:
            return keylist, 9
        if key_size == 196:
            return keylist, 11
        if key_size == 256:
            return keylist, 13

    def subbytes(self, state):
        # TODO
        pass

    def shift_rows(self, state):
        # TODO
        pass

    def mix_columns(self, state):
        new_state = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        n = 8
        mod = BitVector(bitstring='100011011')  # x^8 + x^4 + x^3 + x + 1
        for y in range(4):
            for x in range(4):
                Yn   = BitVector(hexstring=state[y][0]).gf_multiply_modular(BitVector(intVal=M_aes[x][0]), mod, n)
                Yn_1 = BitVector(hexstring=state[y][1]).gf_multiply_modular(BitVector(intVal=M_aes[x][1]), mod, n)
                Yn_2 = BitVector(hexstring=state[y][2]).gf_multiply_modular(BitVector(intVal=M_aes[x][2]), mod, n)
                Yn_3 = BitVector(hexstring=state[y][3]).gf_multiply_modular(BitVector(intVal=M_aes[x][3]), mod, n)
                xored = Yn ^ Yn_1 ^ Yn_2 ^ Yn_3
                new_state[x][y] = (xored.get_bitvector_in_hex())
        return new_state

    def add_round_key(self, state, key_round):
        for i in range(4):
            for j in range(4):
                pass
                # state[i][j] ^= key_round[i][j]

    def tap_into_matrix(self, content):
        shaped_array, state = self.sort_array_to_matrix_state(content)
        for x in range(4):
            for i in range(len(state)):
                if i % 4 == x:
                    shaped_array.append(state[i])
        matrix = [[x for x in shaped_array[i:i + 4]] for i in range(0, len(shaped_array), 4)]
        return matrix

    def sort_array_to_matrix_state(self, content):
        s = " ".join(content[i:i + 2] for i in range(0, len(content), 2))
        state = [x for x in s.split()]
        shaped_array = []
        # sorted array
        return shaped_array, state


if __name__ == '__main__':
    # dont need to convert this, since already hex
    key = "2b7e151628aed2a6abf7158809cf4f3c"  # .encode("utf-8").hex()
    plaintext = "3243f6a8885a308d313198a2e0370734"  # .encode("utf-8").hex()
    cipher = Cipher(key, plaintext, 128)

    cipher.Encrypt()
