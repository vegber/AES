from collections import deque

import S_BOX as sb
from AES import Cipher

# key = "2b7e151628aed2a6abf7158809cf4f3c"
key = "5468617473206D79204B756E67204675"

""" 
Round key simulation. 
"""

keys = []
aes = Cipher(key, "doesent_madder", 128)

matrix = aes.tap_into_matrix(key)  # key is now on matrix form
keys.append(matrix)


# print(keys)

def getRconValue(num):
    """Retrieves a given Rcon Value"""
    return sb.Rcon[num]


def subBytes(state):
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


def matrixify(colums_):
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


def round_key_gen(key: list):
    """
    Input masterkey in matrix form
    :param key:
    :return:
    """
    # for each round, create new matrix
    # first column is last matrix colum xored with
    # find rotWord:
    for round_matrices in range(10):
        colums_ = []
        for col in range(4):
            last_matrix = keys[round_matrices]
            RotWord = [x[3] for x in last_matrix]
            # rotate RotWord
            deqlist = deque(RotWord)
            deqlist.rotate(-1)
            RotWord = list(deqlist)
            nth_column_of_last_matrix = get_nth_column(col, last_matrix)
            if col == 0:  # only first round need a xor b xor c
                # rotated_
                # now SubBytes_
                subbytes_var = subBytes(RotWord)
                # now we xor first column in last matrix
                # with subbytes column
                # and with first column of Rcon
                # rcon is two dimensional
                rcon = [x for x in sb.Rcon[round_matrices]]

                column_of_matrix = [
                    (hex(int(subbytes_var[i], 16) ^ int(nth_column_of_last_matrix[i], 16) ^ int(rcon[i], 16))).lstrip(
                        "0x") for i in range(4)]
                colums_.append(column_of_matrix)
            else:  # last column xor last_mastrix_i
                # todo
                other_colums = [hex(int(nth_column_of_last_matrix[i], 16) ^ int(colums_[col - 1][i], 16)).lstrip("0x")
                                for i in range(4)]
                colums_.append(other_colums)

        # make colums into correct matrix
        # todo
        correct_format = matrixify(colums_)
        keys.append(correct_format)


def get_nth_column(col, last_matrix):

    column = [x[col] for x in last_matrix]
    for val in range(len(column)):
        if column[val] == '':
            column[val] += '0'

    return column


if __name__ == '__main__':
    round_key_gen(matrix)
    for x in keys:
        for y in x:
            print(y)
        print("\n")
