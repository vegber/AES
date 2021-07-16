#!/usr/bin/env python3
"""
All the helper functions we need for encryption and
decryption.

- ASCII to HEX
- stream to blocks (128 bit blocks)
- HEX to ASCII values
- PADDING
"""
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


def stream_to_blocks(block):
    blocks = [block[i:i + 32] for i in range(0, len(block), 32)]
    # pad the last block
    last_block = blocks[-1]
    if len(last_block) != 32:
        padding_scheme(blocks, last_block, 128)
        return blocks
    else:
        return blocks


def padding_scheme(blocks, last_block, bit):
    # pad
    bit_obj = pad_one_block(last_block, bit)
    blocks[-1] = bit_obj.get_bitvector_in_hex()


def pad_one_block(last_block, bit):
    """
    Has hexstring as input!
    :param last_block:
    :return:
    """
    bit_obj = BitVector(hexstring=last_block)
    bit_obj.pad_from_right(bit - len(bit_obj))
    return bit_obj


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

def two_by_two_to_str(two_by_two):
    out = ""
    transposed_list = transpose(two_by_two)
    for x in transposed_list:
        for y in x:
            out += y
    return out

def transpose(nested_list):
    transpose = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for x in range(4):
        for y in range(4):
            transpose[y][x] = nested_list[x][y]
    return transpose

def read_from_file(file_name):
    return open(file_name, 'r+')

def format_content(content: list, content_encoding: bool) -> list:
    """
    - iterate trough content, and make it into one string
    - if not in hex, convert to hex
    - then turn string to blocks with padding
    :param content:
    :param content_encoding:
    :return:
    """
    content_str = ""
    for x in content:
        content_str += x
    if content_encoding:
        content_str = ascii_to_hex(content_str)
    return stream_to_blocks(content_str)

def write_to_file(content, filename):
    with open(filename, 'w+') as file:
        file.write(content)

