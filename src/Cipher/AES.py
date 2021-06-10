from collections import deque

import static.S_BOX as sb


class Cipher:
    keys = []
    state = []
    rounds = 0

    def __init__(self, key, plaintext, key_size):
        self.key = key  # Key is n bits
        self.plaintext = plaintext
        self.key_size = key_size
        self.keys.append(self.tap_into_matrix(key))
        self.round_key_gen(self.tap_into_matrix(key))

    def Encrypt(self):
        # Call upon keygen
        # turn plaintext to "matrix"
        self.state = self.tap_into_matrix(self.plaintext)
        self.printable()
        self.add_round_key()
        self.printable()
        for x in range(9):  # n -1 rounds
            self.round_encyption()
            # Now last round
        self.last_round()
        return self.state

    def last_round(self):
        self.subbytes()
        self.printable()
        self.shift_rows()
        self.printable()
        self.add_round_key()
        self.printable()

    def round_encyption(self):
        self.subbytes()
        self.printable()
        self.shift_rows()
        self.printable()
        self.mix_columns()
        self.printable()
        self.add_round_key()
        self.printable()

    def printable(self):
        print(*self.state, sep='\n')
        print()

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

    def subbytes(self):
        # TODO
        new_list = []
        print("wer here")
        print(self.state)
        # variable_change = [hex(sb.Sbox[int(y, 16)]).lstrip("0x") for y in lists]
        # new_list.append(variable_change)
        self.state = new_list

    def shift_rows(self):
        # TODO
        shifted_rows = []
        for x in range(len(self.state)):
            if x == 0:
                shifted_rows.append(self.state[x])
            else:
                vector = deque(self.state[x])
                vector.rotate(-x)
                listed_vector = list(vector)
                shifted_rows.append(listed_vector)
        self.state = shifted_rows

    def mix_columns(self):
        a = [[self.state[x][0] for x in range(4)], [self.state[x][1] for x in range(4)],
             [self.state[x][2] for x in range(4)], [self.state[x][3] for x in range(4)]]
        cop = []
        for x in a:
            cop.append(self.colum_mix_colum(int(x[0], 16), int(x[1], 16), int(x[2], 16), int(x[3], 16)))
        rotate = self.matrixify(cop)
        self.state = rotate

    def colum_mix_colum(self, a, b, c, d):
        one = (self.gmul(a, 2) ^ self.gmul(b, 3) ^ self.gmul(c, 1) ^ self.gmul(d, 1))
        two = (self.gmul(a, 1) ^ self.gmul(b, 2) ^ self.gmul(c, 3) ^ self.gmul(d, 1))
        three = (self.gmul(a, 1) ^ self.gmul(b, 1) ^ self.gmul(c, 2) ^ self.gmul(d, 3))
        four = (self.gmul(a, 3) ^ self.gmul(b, 1) ^ self.gmul(c, 1) ^ self.gmul(d, 2))
        return [hex(one).lstrip("0x"), hex(two).lstrip("0x"), hex(three).lstrip("0x"), hex(four).lstrip("0x")]

    def gmul(self, a, b):
        if b == 1:
            return a
        tmp = (a << 1) & 0xff
        if b == 2:
            return tmp if a < 128 else tmp ^ 0x1b
        if b == 3:
            return self.gmul(a, 2) ^ a

    def add_round_key(self):
        print(f"Round_key at {self.rounds} with key: {self.keys[self.rounds]}")
        for i in range(4):
            for j in range(4):
                if self.state[i][j] == '':
                    self.state[i][j] += '0'
                self.state[i][j] = hex(int(self.state[i][j], 16) ^ int(self.keys[self.rounds][i][j], 16)).lstrip("0x")

        self.rounds += 1

    def tap_into_matrix(self, content):
        shaped_array, state = self.sort_array_to_matrix_state(content)
        for x in range(4):
            for i in range(len(state)):
                if i % 4 == x:
                    shaped_array.append(state[i])
        matrix = [[x for x in shaped_array[i:i + 4]] for i in range(0, len(shaped_array), 4)]
        return matrix

    @staticmethod
    def sort_array_to_matrix_state(content):
        s = " ".join(content[i:i + 2] for i in range(0, len(content), 2))
        state = [x for x in s.split()]
        shaped_array = []
        # sorted array
        return shaped_array, state

    def matrixify(self, colums_):
        ret_me = []
        a = []
        b = []
        c = []
        d = []
        for x in range(len(colums_)):
            a.append(colums_[x][0])
            b.append(colums_[x][1])
            c.append(colums_[x][2])
            d.append(colums_[x][3])
        ret_me.append(a)
        ret_me.append(b)
        ret_me.append(c)
        ret_me.append(d)
        return ret_me

    def subBytes_for_roundkeys(self, state):
        # for byte in state:
        #    print("0x"+byte)
        # var = [sb.Sbox[binascii.hexlify(byte)] for byte in state]
        # todo
        # bug where some state contains empty string
        try:
            for index in range(len(state)):
                if state[index] == '':
                    state[index] += '0'
            return [hex(sb.Sbox[int("0x" + word, 16)]) for word in state]
        except:
            print(f"Error at: {state}")

    @staticmethod
    def get_nth_column(col, last_matrix):

        column = [x[col] for x in last_matrix]
        for val in range(len(column)):
            if column[val] == '':
                column[val] += '0'

        return column

    def round_key_gen(self, key: list):
        """
        Input masterkey in matrix form
        :param key:
        :return:
        """
        # for each round, create new matrix
        # first column is last matrix column xor with
        # find rotWord:
        for round_matrices in range(10):
            colums_ = []
            for col in range(4):
                last_matrix = self.keys[round_matrices]
                RotWord = [x[3] for x in last_matrix]
                # rotate RotWord
                deqlist = deque(RotWord)
                deqlist.rotate(-1)
                RotWord = list(deqlist)
                nth_column_of_last_matrix = self.get_nth_column(col, last_matrix)
                if col == 0:  # only first round need a xor b xor c
                    # rotated_
                    # now SubBytes_
                    subbytes_var = self.subBytes_for_roundkeys(RotWord)
                    # now we xor first column in last matrix
                    # with subbytes column
                    # and with first column of Rcon
                    # rcon is two dimensional
                    rcon = [x for x in sb.Rcon[round_matrices]]
                    column_of_matrix = [
                        (hex(int(subbytes_var[i], 16) ^ int(nth_column_of_last_matrix[i], 16) ^ int(rcon[i],
                                                                                                    16))).lstrip(
                            "0x") for i in range(4)]
                    colums_.append(column_of_matrix)
                else:  # last column xor last_mastrix_i
                    # todo
                    other_colums = [
                        hex(int(nth_column_of_last_matrix[i], 16) ^ int(colums_[col - 1][i], 16)).lstrip("0x")
                        for i in range(4)]
                    for index in range(len(other_colums)):
                        if other_colums[index] == '':
                            other_colums[index] = "0"
                    colums_.append(other_colums)
            # make colums into correct matrix
            # todo
            correct_format = self.matrixify(colums_)
            self.keys.append(correct_format)


if __name__ == '__main__':
    # dont need to convert this, since already hex
    key = "2b7e151628aed2a6abf7158809cf4f3c"  # .encode("utf-8").hex()
    plaintext = "3243f6a8885a308d313198a2e0370734"  # .encode("utf-8").hex()
    cipher = Cipher(key, plaintext, 128)

    cipher.Encrypt()

