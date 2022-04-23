# Copyright 2021 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from utapi.datalink.datalink_api_can import DataLinkApiCan


def print_help():
    print("Select the communication interface")
    print("./demo2_datalink_can arg1")
    print("    [arg1] 1: DataLink TCP To CAN")
    print("           2: DataLink UDP To CAN")
    print("           3: DataLink USB To CAN")


def main():
    u"""This example tests the EtherNet to CAN module, sends the received CAN data back.
    """
    if len(sys.argv) != 2:
        print_help()
        return

    ip = "192.168.1.166"
    com = "/dev/ttyACM0"

    if int(sys.argv[1]) == 1:
        datalink = DataLinkApiCan(1, [ip, 6001, 5001], 1)
        if datalink.is_error():
            return

    elif int(sys.argv[1]) == 2:
        datalink = DataLinkApiCan(2, [ip, 6001, 5001], 1)
        if datalink.is_error():
            return

    elif int(sys.argv[1]) == 3:
        datalink = DataLinkApiCan(3, [com, 921600], 1)
        if datalink.is_error():
            return
    else:
        print_help()
        return

    while(1):
        ret = datalink.read()
        if ret != -1:
            print("recv: id = %d, len = %d, data = " % (ret[0], ret[1]), ret[2])
            datalink.write(ret[0], ret[1], ret[2])


if __name__ == '__main__':
    main()
