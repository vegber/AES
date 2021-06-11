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
        self.round_key_gen()

    def Encrypt(self):
        # Call upon keygen
        # turn plaintext to "matrix"
        self.state = self.tap_into_matrix(self.plaintext)
        self.add_round_key()
        for x in range(9):  # n -1 rounds
            self.round_encryption()
            # Now last round
        self.last_round()
        return self.state

    def last_round(self):
        self.substitute_bytes()
        self.shift_rows()
        self.add_round_key()

    def round_encryption(self):
        self.substitute_bytes()
        self.shift_rows()
        self.mix_columns()
        self.add_round_key()

    def printable(self):
        print(*self.state, sep='\n')
        print()

    def round_keys(self, key, key_size):
        # TODO
        # key to matrix form
        # generate all the round keys
        # update the keys[] list
        self.keys.append(self.tap_into_matrix(key))
        kwlist = []
        if key_size == 128:
            return kwlist, 9
        if key_size == 196:
            return kwlist, 11
        if key_size == 256:
            return kwlist, 13

    def substitute_bytes(self):
        # TODO
        new_list = []
        for x in self.state:
            between_stage = []
            for y in x:
                if y == '':
                    between_stage.append(hex(sb.Sbox[int('0', 16)]).lstrip("0x"))
                else:
                    between_stage.append(hex(sb.Sbox[int(y, 16)]).lstrip("0x"))
            new_list.append(between_stage)
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
            cop.append(self.column_mix_column(int(x[0], 16), int(x[1], 16), int(x[2], 16), int(x[3], 16)))
        rotate = self.convert_to_matrix(cop)
        self.state = rotate

    def column_mix_column(self, a, b, c, d):
        one = (self.galoisfield_multiplication(a, 2) ^ self.galoisfield_multiplication(b, 3) ^ self.galoisfield_multiplication(c, 1) ^ self.galoisfield_multiplication(d, 1))
        two = (self.galoisfield_multiplication(a, 1) ^ self.galoisfield_multiplication(b, 2) ^ self.galoisfield_multiplication(c, 3) ^ self.galoisfield_multiplication(d, 1))
        three = (self.galoisfield_multiplication(a, 1) ^ self.galoisfield_multiplication(b, 1) ^ self.galoisfield_multiplication(c, 2) ^ self.galoisfield_multiplication(d, 3))
        four = (self.galoisfield_multiplication(a, 3) ^ self.galoisfield_multiplication(b, 1) ^ self.galoisfield_multiplication(c, 1) ^ self.galoisfield_multiplication(d, 2))
        return [hex(one).lstrip("0x"), hex(two).lstrip("0x"), hex(three).lstrip("0x"), hex(four).lstrip("0x")]

    def galoisfield_multiplication(self, a, b):
        if b == 1:
            return a
        tmp = (a << 1) & 0xff
        if b == 2:
            return tmp if a < 128 else tmp ^ 0x1b
        if b == 3:
            return self.galoisfield_multiplication(a, 2) ^ a

    def add_round_key(self):
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

    @staticmethod
    def convert_to_matrix(columns_):
        ret_me = []
        a = []
        b = []
        c = []
        d = []
        for x in range(len(columns_)):
            a.append(columns_[x][0])
            b.append(columns_[x][1])
            c.append(columns_[x][2])
            d.append(columns_[x][3])
        ret_me.append(a)
        ret_me.append(b)
        ret_me.append(c)
        ret_me.append(d)
        return ret_me

    @staticmethod
    def subBytes_for_round_keys(state):
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
        except "Substitution ERROR":
            print(f"Error at: {state}")

    @staticmethod
    def get_nth_column(col, last_matrix):
        column = [x[col] for x in last_matrix]
        for val in range(len(column)):
            if column[val] == '':
                column[val] += '0'
        return column

    def round_key_gen(self):
        """
        Input masterkey in matrix form
        :return:
        """
        # for each round, create new matrix
        # first column is last matrix column xor with
        # find rotWord:
        for round_matrices in range(10):
            columns_ = []
            for col in range(4):
                last_matrix = self.keys[round_matrices]
                RotWord = [x[3] for x in last_matrix]
                # rotate RotWord
                dequelist = deque(RotWord)
                dequelist.rotate(-1)
                RotWord = list(dequelist)
                nth_column_of_last_matrix = self.get_nth_column(col, last_matrix)
                if col == 0:  # only first round need a xor b xor c
                    # rotated_
                    # now SubBytes_
                    subbytes_var = self.subBytes_for_round_keys(RotWord)
                    # now we xor first column in last matrix
                    # with Substitute bytes column
                    # and with first column of R_con
                    # r_con is two dimensional
                    rcon = [x for x in sb.Rcon[round_matrices]]
                    column_of_matrix = [
                        (hex(int(subbytes_var[i], 16) ^ int(nth_column_of_last_matrix[i], 16) ^ int(rcon[i],
                                                                                                    16))).lstrip(
                            "0x") for i in range(4)]
                    columns_.append(column_of_matrix)
                else:  # last column xor last_matrix
                    other_colums = [
                        hex(int(nth_column_of_last_matrix[i], 16) ^ int(columns_[col - 1][i], 16)).lstrip("0x")
                        for i in range(4)]
                    for index in range(len(other_colums)):
                        if other_colums[index] == '':
                            other_colums[index] = "0"
                    columns_.append(other_colums)
            # make colums into correct matrix
            correct_format = self.convert_to_matrix(columns_)
            self.keys.append(correct_format)


if __name__ == '__main__':
    # dont need to convert this, since already hex
    key_master = "2b7e151628aed2a6abf7158809cf4f3c"  # .encode("utf-8").hex()
    plaintext_ = "3243f6a8885a308d313198a2e0370734"  # .encode("utf-8").hex()
    cipher = Cipher(key_master, plaintext_, 128)

    cipher.Encrypt()
    cipher.printable()
