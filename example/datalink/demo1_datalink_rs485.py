#!/usr/bin/env python3
#
# Copyright (C) 2021 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from utapi.datalink.datalink_api_rs485 import DataLinkApiRs485


def print_help():
    print("Select the communication interface")
    print("./demo1_datalink_rs485 arg1")
    print("    [arg1] 1: DataLink TCP To RS485")
    print("           2: DataLink UDP To RS485")
    print("           3: DataLink USB To RS485")


def main():
    u"""This example tests the EtherNet to RS485 module, sends the received RS485 data back.
    """
    if len(sys.argv) != 2:
        print_help()
        return

    ip = "192.168.1.168"
    com = "/dev/ttyACM0"

    if int(sys.argv[1]) == 1:
        datalink = DataLinkApiRs485(1, [ip, 6001, 5001], 1, 921600)
        if datalink.is_error():
            return

    elif int(sys.argv[1]) == 2:
        datalink = DataLinkApiRs485(2, [ip, 6001, 5001], 1, 921600)
        if datalink.is_error():
            return

    elif int(sys.argv[1]) == 3:
        datalink = DataLinkApiRs485(3, [com, 921600], 1)
        if datalink.is_error():
            return
    else:
        print_help()
        return

    while(1):
        ret = datalink.read()
        if len(ret) > 0:
            print("recv: ", ret)
            datalink.write(ret)


if __name__ == '__main__':
    main()
