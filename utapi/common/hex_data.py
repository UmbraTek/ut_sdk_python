#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================

import struct


def bytes_to_int8(data, num=1):
    if num == 1:
        str1 = struct.unpack("<b", bytes([data]))
        return str1[0]

    ret = [0] * num
    for i in range(num):
        byte = bytes([data[i]])
        str1 = struct.unpack("<b", byte)
        ret[i] = str1[0]
    return ret


def bytes_to_int16_big(data):
    byte = bytes([data[0]])
    byte += bytes([data[1]])
    str1 = struct.unpack(">h", byte)
    return str1[0]


def bytes_to_uint16_big(data):
    byte = bytes([data[0]])
    byte += bytes([data[1]])
    str1 = struct.unpack(">H", byte)
    return str1[0]


def bytes_to_uint24_big(data):
    byte = bytes([0])
    byte += bytes([data[0]])
    byte += bytes([data[1]])
    byte += bytes([data[2]])
    str1 = struct.unpack(">I", byte)
    return str1[0]


"""
def bytes_to_int32_big(data):
    byte = bytes([data[0]])
    byte += bytes([data[1]])
    byte += bytes([data[2]])
    byte += bytes([data[3]])
    str1 = struct.unpack(">i", byte)
    return str1[0]
"""


def bytes_to_int32_big(data, num=1):
    ret = [0] * num
    for i in range(num):
        byte = bytes([data[i * 4]])
        byte += bytes([data[i * 4 + 1]])
        byte += bytes([data[i * 4 + 2]])
        byte += bytes([data[i * 4 + 3]])
        str1 = struct.unpack(">i", byte)
        ret[i] = str1[0]

    if num == 1:
        return ret[0]
    else:
        return ret


def bytes_to_uint32_big(data, num=1):
    ret = [0] * num
    for i in range(num):
        byte = bytes([data[i * 4]])
        byte += bytes([data[i * 4 + 1]])
        byte += bytes([data[i * 4 + 2]])
        byte += bytes([data[i * 4 + 3]])
        str1 = struct.unpack(">I", byte)
        ret[i] = str1[0]

    if num == 1:
        return ret[0]
    else:
        return ret


"""
def int8_to_bytes_big(data):
    str1 = bytes(struct.pack(">b", data))
    return str1
"""


def int8_to_bytes_big(data, num=1):
    if num == 1:
        str1 = bytes(struct.pack(">b", data))
        return str1
    else:
        str1 = bytes(struct.pack(">b", data[0]))
        for i in range(num - 1):
            str1 += bytes(struct.pack(">b", data[i + 1]))
    return str1


def uint8_to_bytes_big(data, num=1):
    if num == 1:
        str1 = bytes(struct.pack(">B", data))
        return str1
    else:
        str1 = bytes(struct.pack(">B", data[0]))
        for i in range(num - 1):
            str1 += bytes(struct.pack(">B", data[i + 1]))
    return str1


def int16_to_bytes_big(data, num=1):
    if num == 1:
        str1 = bytes(struct.pack(">h", data))
        return str1
    else:
        str1 = bytes(struct.pack(">h", data[0]))
        for i in range(num - 1):
            str1 += bytes(struct.pack(">h", data[i + 1]))
    return str1


def uint16_to_bytes_big(data, num=1):
    if num == 1:
        str1 = bytes(struct.pack(">H", data))
        return str1
    else:
        str1 = bytes(struct.pack(">H", data[0]))
        for i in range(num - 1):
            str1 += bytes(struct.pack(">H", data[i + 1]))
    return str1


'''
def int32_to_bytes_big(data):
    str1 = bytes(struct.pack(">i", data))
    return str1
'''


def int32_to_bytes_big(data, num=1):
    if num == 1:
        str1 = bytes(struct.pack(">i", data))
        return str1
    else:
        str1 = bytes(struct.pack(">i", data[0]))
        for i in range(num - 1):
            str1 += bytes(struct.pack(">i", data[i + 1]))
    return str1


def uint32_to_bytes_big(data, num=1):
    if num == 1:
        str1 = bytes(struct.pack(">I", data))
        return str1
    else:
        str1 = bytes(struct.pack(">I", data[0]))
        for i in range(num - 1):
            str1 += bytes(struct.pack(">I", data[i + 1]))
    return str1


def fp32_to_bytes_big(data, num=1):
    if num == 1:
        str1 = bytes(struct.pack(">f", data))
        return str1
    else:
        str1 = bytes(struct.pack(">f", data[0]))
        for i in range(1, num):
            str1 += bytes(struct.pack(">f", data[i]))
        return str1


def bytes_to_fp32_big(data, num=1):
    ret = [0] * num
    for i in range(num):
        byte = bytes([data[i * 4]])
        byte += bytes([data[i * 4 + 1]])
        byte += bytes([data[i * 4 + 2]])
        byte += bytes([data[i * 4 + 3]])
        str1 = struct.unpack(">f", byte)
        ret[i] = str1[0]

    if num == 1:
        return ret[0]
    else:
        return ret


def bytes_to_fp32(data, num=1):
    ret = [0] * num
    for i in range(num):
        byte = bytes([data[i * 4]])
        byte += bytes([data[i * 4 + 1]])
        byte += bytes([data[i * 4 + 2]])
        byte += bytes([data[i * 4 + 3]])
        str1 = struct.unpack("<f", byte)
        ret[i] = str1[0]

    if num == 1:
        return ret[0]
    else:
        return ret
