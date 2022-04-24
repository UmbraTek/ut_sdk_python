# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from common import print_msg
from common import hex_data
from common import crc16
from common import hex_data


class UTCC_RX_ERROR():
    HEAD = -1
    ID = -2
    TIMEOUT = -3
    STATE = -4
    LEN = -5
    RW = -6
    CMD = -7
    CRC = -8
    CONNECT = -9

    def __init__(self):
        pass


class UTCC_RW:
    R = 0
    W = 1


class UtccType():
    def __init__(self):
        self.head = 0xAA
        self.state = 0
        self.id = 0
        self.len = 0
        self.rw = 0
        self.cmd = 0
        self.data = [0] * 125
        self.crc = [0] * 2

        self.buf = bytes([0])

    def pack(self):
        self.buf = bytes([self.head])
        self.buf += hex_data.uint16_to_bytes_big(((self.state & 0x01) << 7) + (self.id & 0x7F))
        self.buf += bytes([self.len])
        self.buf += bytes([((self.rw & 0x01) << 7) + (self.cmd & 0x7F)])

        for i in range(self.len - 1):
            self.buf += bytes([self.data[i]])

        self.crc = crc16.crc_modbus(self.buf)
        self.buf += self.crc
        return self.buf

    def unpack(self, buf):
        self.buf = buf
        if len(buf) < 7:
            print("[UtccTyp] Error: UTCC_RX_ERROR.LEN: %d" % (len(buf)))
            return UTCC_RX_ERROR.LEN

        self.len = buf[3] & 0x0F
        # if self.len + 6 != len(buf):
        #    return UTCC_RX_ERROR.LEN

        if self.head != buf[0]:
            print("[UtccTyp] Error: UTCC_RX_ERROR.HEAD: %d %d" % (self.head, buf[0]))
            return UTCC_RX_ERROR.HEAD

        id = hex_data.bytes_to_uint16_big(buf[1:3])
        self.state = (id & 0x80) >> 7
        self.id = id & 0x7F
        self.rw = (buf[4] & 0x80) >> 7
        self.cmd = buf[4] & 0x7F

        data_len = self.len - 1
        if data_len > 7:
            data_len = 7
        for i in range(data_len):
            self.data[i] = buf[5 + i]

        self.crc[0] = buf[self.len + 4]
        self.crc[1] = buf[self.len + 5]
        temp1 = hex_data.bytes_to_uint16_big(self.crc)
        crc = crc16.crc_modbus(buf[0:self.len + 4])
        temp2 = hex_data.bytes_to_uint16_big(crc)
        if temp1 != temp2:
            return UTCC_RX_ERROR.CRC
        return 0

    def print_pack(self):
        print("\n[utcc pack]")
        print("head : 0x%x" % (self.head))
        print("state: 0x%x" % (self.state))
        print("id   : %d" % (self.id))
        print("len  : %d" % (self.len))
        print("rw   : %d" % (self.rw))
        print("cmd  : %d" % (self.cmd))
        if self.len > 1:
            print_msg.nhex("data : ", self.data, self.len - 1)
        print("crc  : 0x%x 0x%x" % (self.crc[0], self.crc[1]))

    def print_buf(self):
        print("\n[utcc buf]")
        print_msg.nhex("buf : ", self.buf, len(self.buf))


class UtccClient():
    def __init__(self, port_fp):
        self.port_fp = port_fp
        self.port_fp.flush()

    def connect_device(self, argv1=0xFFFFFFFF):
        tx_utcc = UtccType()
        tx_utcc.head = 0xAA
        tx_utcc.id = 0x0055
        tx_utcc.state = 0
        tx_utcc.len = 0x08
        tx_utcc.rw = 0
        tx_utcc.cmd = 0x7F
        tx_utcc.data[0:8] = [0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F]
        tx_utcc.data[0:4] = hex_data.uint32_to_bytes_big(argv1)
        # print(argv1)
        # print(tx_utcc.data[0:8])

        self.send(tx_utcc)
        ret, rx_utcc = self.pend(tx_utcc, 1, 2)
        if ret != 0:
            return ret
        return 0

    def send(self, tx_utcc):
        buf = tx_utcc.pack()
        self.port_fp.flush()
        self.port_fp.write(buf)
        # print_msg.nhex("MxBus send_xbus buf : ", buf, len(buf))

    def _pend(self, tx_utcc, timeout):
        """
        timeout：ms
        """
        rx_utcc = UtccType()
        ret = UTCC_RX_ERROR.TIMEOUT
        rx_data = self.port_fp.read(int(timeout))
        if rx_data == -1 or len(rx_data) < 7:
            return (ret, rx_utcc)

        # print_msg.nhex("[UtccCil] rx_data : ", rx_data, len(rx_data))
        ret = rx_utcc.unpack(rx_data)
        if ret != 0:
            return (ret, rx_utcc)
        elif tx_utcc.id != rx_utcc.id:
            print("[UtccCil] Error: tx_utcc.id = 0x%x, rx_utcc.id= 0x%x" % (tx_utcc.id, rx_utcc.id))
            ret = UTCC_RX_ERROR.ID
        elif rx_utcc.state != 0:
            ret = UTCC_RX_ERROR.STATE
        elif tx_utcc.rw != rx_utcc.rw:
            print("[UtccCil] Error: tx_utcc.rw: 0x%x, rx_utcc.rw: %x" % (tx_utcc.rw, rx_utcc.rw))
            ret = UTCC_RX_ERROR.RW
        elif tx_utcc.cmd != rx_utcc.cmd:
            print("[UtccCil] Error: tx_utcc.cmd: 0x%x, rx_utcc.cmd: %x" % (tx_utcc.cmd, rx_utcc.cmd))
            ret = UTCC_RX_ERROR.CMD

        return (ret, rx_utcc)

    def pend(self, tx_utcc, rx_len, timeout):
        rx_utcc1 = -1
        while(1):
            ret, rx_utcc2 = self._pend(tx_utcc, timeout)
            if ret != 0 and ret != UTCC_RX_ERROR.STATE:
                return ret, rx_utcc2

            if rx_utcc1 == -1:
                rx_utcc1 = rx_utcc2
            else:
                rx_utcc1.data = rx_utcc1.data[0:rx_utcc1.len - 1] + rx_utcc2.data[0:rx_utcc2.len - 1]
                rx_utcc1.len = rx_utcc1.len + rx_utcc2.len - 1

            if rx_utcc1.len == rx_len + 1:
                return ret, rx_utcc1


class UTCC_RXSTART:
    FROMID = 0
    TOID1 = 1
    TOID2 = 2
    LEN = 3
    DATA = 4
    CRC1 = 5
    CRC2 = 6
    RXLEN_MAX = 64


class UtccDecode:
    def __init__(self, fromid, toid):
        self.DB_FLG = "[utcc dec] "
        self.flush(fromid, toid)

    # wipe cache , set from_id and to_id
    def flush(self, fromid=-1, toid=-1):
        self.rxstate = UTCC_RXSTART.FROMID
        self.data_idx = 0
        self.len = 0
        if fromid != -1:
            self.fromid = fromid
        if toid != -1:
            self.toid = toid

    def put(self, rxstr, length, rx_que):
        if length == 0:
            length = len(rxstr)
        if len(rxstr) < length:
            print(self.DB_FLG + "error: len(rxstr) < length")

        for i in range(length):
            rxch = bytes([rxstr[i]])
            # print_msg.nhex(self.DB_FLG, rxch, 1)
            # print('state:%d' % (self.rxstate))
            if UTCC_RXSTART.FROMID == self.rxstate:
                if self.fromid == rxch[0] or self.fromid == 0x55:
                    self.rxbuf = rxch
                    self.rxstate = UTCC_RXSTART.TOID1

            elif UTCC_RXSTART.TOID1 == self.rxstate:
                self.rxbuf += rxch
                self.rxstate = UTCC_RXSTART.TOID2

            elif UTCC_RXSTART.TOID2 == self.rxstate:
                self.rxbuf += rxch
                self.rxstate = UTCC_RXSTART.LEN

            elif UTCC_RXSTART.LEN == self.rxstate:
                if (rxch[0] & 0x7F) < UTCC_RXSTART.RXLEN_MAX:
                    self.rxbuf += rxch
                    self.len = rxch[0] & 0x7F
                    self.data_idx = 0
                    self.rxstate = UTCC_RXSTART.DATA
                else:
                    self.rxstate = UTCC_RXSTART.FROMID

            elif UTCC_RXSTART.DATA == self.rxstate:
                if self.data_idx < self.len:
                    self.rxbuf += rxch
                    self.data_idx += 1
                    if self.data_idx == self.len:
                        self.rxstate = UTCC_RXSTART.CRC1
                else:
                    self.rxstate = UTCC_RXSTART.FROMID

            elif UTCC_RXSTART.CRC1 == self.rxstate:
                self.rxbuf += rxch
                self.rxstate = UTCC_RXSTART.CRC2

            elif UTCC_RXSTART.CRC2 == self.rxstate:
                self.rxbuf += rxch
                self.rxstate = UTCC_RXSTART.FROMID
                crc = crc16.crc_modbus(self.rxbuf[:self.len + 4])
                if crc[0] == self.rxbuf[self.len + 4] and crc[1] == self.rxbuf[self.len + 5]:
                    if rx_que.full():
                        rx_que.get()
                    rx_que.put(self.rxbuf)
                    # print_msg.nhex("[SockSeri] rx_que.put: ", self.rxbuf, len(self.rxbuf))
