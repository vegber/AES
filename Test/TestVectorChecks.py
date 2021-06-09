import Cipher


def first_checker():
    cipher_key = "2b7e151628aed2a6abf7158809cf4f3c"
    plain = "3243f6a8885a308d313198a2e0370734"
    plaintext_matrix = [['32', '88', '31', 'e0'], ['43', '5a', '31', '37'], ['f6', '30', '98', '07'],
                        ['a8', '8d', 'a2', '34']]
    # todo
    # check, correct sorting
    # correct matrix form
    # TODO

    cipher = Cipher(cipher_key, plain, 128)
    assert cipher.tap_into_matrix(plain) == plaintext_matrix, "Should be a four by four matrix"
