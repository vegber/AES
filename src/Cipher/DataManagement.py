"""
All the helper functions we need for encryption and
decryption.

- ASCII to HEX
- stream to blocks (128 bit blocks)
- HEX to ASCII values
- PADDING
"""
from binascii import *

from BitVector import *


def ascii_to_hex(input):
    """
    This function will not work on big cases due to memory
    :param input:
    :return: input as hex
    """
    return input.encode().hex()


def hex_to_ascii(input):
    """
    This function will turn hex to ascii
    :param input:
    :return:
    """
    return bytes.fromhex(input).decode('utf-8')


def divideString(string, n):
    pass


def stream_to_blocks(block):
    blocks = [block[i:i + 32] for i in range(0, len(block), 32)]
    # pad the last block
    last_block = blocks[-1]
    if len(last_block) != 32:
        # pad
        bit_obj = BitVector(hexstring=last_block)
        bit_obj.pad_from_right(128 - len(bit_obj))
        blocks[-1] = bit_obj.get_bitvector_in_hex()
        return blocks
    else:
        return blocks

def remove_padding(blocks: str):
    """
    Ill use the fact that all padding will be
    trailing zeros.
    Since my hex values are strings, this is
    quite simple
    ONLY USE FOR THE LAST BLOCK
    :param blocks:
    :return:
    """
    return blocks.rstrip("0")


def zeroesUpToN(n):
    zeros = 0
    for i in range(len(n)):
        s = n[i]
        zeros += s.count('0')
    return zeros

"""
key_master = "2b7e151628aed2a6abf7158809cf4f3c"  # .encode("utf-8").hex()
plaintext_ = "3243f6a8885a308d313198a2e0370734"  # .encode("utf-8").hex()
cipher_text = "3925841d02dc09fbdc118597196a0b32"
"""
