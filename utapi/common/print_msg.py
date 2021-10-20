# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================


def nhex(str1, data, len1):
    for i in range(len1):
        str1 += "0x%0.2X " % data[i]
    print(str1)


def nvect_03f(str1, data, len1):
    for i in range(len1):
        str1 += "%0.3f " % data[i]
    print(str1)


def nvect_03f_get(str1, data, len1):
    for i in range(len1):
        str1 += "%0.3f " % data[i]
    return str1


def nvect_int(str1, data, len1):
    for i in range(len1):
        str1 += "%d " % data[i]
    print(str1)


def nvect_06f(str1, data, len1):
    for i in range(len1):
        str1 += "%0.6f " % data[i]
    print(str1)


def nvect_f(str1, data, len1):
    for i in range(len1):
        str1 += "%f " % data[i]
    print(str1)
