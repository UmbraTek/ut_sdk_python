# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from common import print_msg
from common import crc16


class UTRC_RX_ERROR:
    M_ID = -1
    S_ID = -2
    TIMEOUT = -3
    STATE = -4
    LEN = -5
    RW = -6
    CMD = -7
    CRC = -8
    CONNECT = -9
    LEN_MIN = -10

    def __init__(self):
        pass


class UTRC_RW:
    R = 0
    W = 1


class UtrcType:
    def __init__(self):
        self.master_id = 0xAA
        self.slave_id = 0
        self.state = 0
        self.len = 0
        self.rw = 0
        self.cmd = 0
        self.data = [0] * 125
        self.crc = [0] * 2

        self.buf = bytes([0])

    def pack(self):
        self.buf = bytes([self.master_id])
        self.buf += bytes([self.slave_id])
        self.buf += bytes([((self.state & 0x01) << 7) + (self.len & 0x7F)])
        self.buf += bytes([((self.rw & 0x01) << 7) + (self.cmd & 0x7F)])

        for i in range(self.len - 1):
            self.buf += bytes([self.data[i]])

        self.crc = crc16.crc_modbus(self.buf)
        self.buf += self.crc
        return self.buf

    def unpack(self, buf):
        self.buf = buf
        if len(buf) < 6:
            print("[UtrcTyp] Error: UTRC_RX_ERROR.LEN: %d" % (len(buf)))
            return UTRC_RX_ERROR.LEN

        self.len = buf[2] & 0x7F
        if self.len + 5 != len(buf):
            print("[UtrcTyp] Error: UTRC_RX_ERROR.LEN: %d %d" % (self.len, len(buf)))
            return UTRC_RX_ERROR.LEN

        self.master_id = buf[0]
        self.slave_id = buf[1]
        self.state = (buf[2] & 0x80) >> 7
        self.rw = (buf[3] & 0x80) >> 7
        self.cmd = buf[3] & 0x7F

        data_len = self.len - 1
        for i in range(data_len):
            self.data[i] = buf[4 + i]

        self.crc[0] = buf[data_len + 4]
        self.crc[1] = buf[data_len + 5]
        return 0

    def print_pack(self):
        print("\n[utrc pack]")
        print("m_id : 0x%x" % (self.master_id))
        print("s_id : 0x%x" % (self.slave_id))
        print("state: %d" % (self.state))
        print("len  : %d" % (self.len))
        print("rw   : %d" % (self.rw))
        print("cmd  : 0x%x" % (self.cmd))
        if self.len > 1:
            print_msg.nhex("data : ", self.data, self.len)
        print("crc  : 0x%x 0x%x" % (self.crc[0], self.crc[1]))

    def print_buf(self):
        print("\n[utrc buf]")
        print_msg.nhex("buf  : ", self.buf, len(self.buf))


class UtrcClient:
    def __init__(self, port_fp):
        self.port_fp = port_fp
        self.port_fp.flush()

    def send(self, tx_utrc):
        buf = tx_utrc.pack()
        # tx_utrc.print_buf()
        self.port_fp.flush(tx_utrc.slave_id, tx_utrc.master_id)
        self.port_fp.write(buf)
        # print_msg.nhex("UtrcClient send_xbus buf : ", buf, len(buf))

    def pend(self, tx_utrc, r_len, timeout_s):
        """
        timeout_s：s
        """
        rx_utrc = UtrcType()
        ret = UTRC_RX_ERROR.TIMEOUT
        rx_data = self.port_fp.read(timeout_s)
        if rx_data == -1 or len(rx_data) < 6:
            return (ret, rx_utrc)

        # print_msg.nhex("NetBus send_pend rx_data : ", rx_data, len(rx_data))
        ret = rx_utrc.unpack(rx_data)
        if ret != 0:
            return (ret, rx_utrc)
        elif rx_utrc.master_id != tx_utrc.slave_id and tx_utrc.slave_id != 0x55:
            print("[UtrcCli] Error: UTRC_RX_ERROR.M_ID: %d %d" % (rx_utrc.master_id, tx_utrc.slave_id))
            ret = UTRC_RX_ERROR.M_ID
        elif rx_utrc.slave_id != tx_utrc.master_id:
            print("[UtrcCli] Error: UTRC_RX_ERROR.S_ID: %d %d" % (rx_utrc.slave_id, tx_utrc.master_id))
            ret = UTRC_RX_ERROR.S_ID
        elif rx_utrc.state != 0:
            ret = UTRC_RX_ERROR.STATE
        elif rx_utrc.len != r_len + 1 and r_len != 0x55:
            print("[UtrcCli] Error: UTRC_RX_ERROR.LEN: %d %d" % (rx_utrc.len, r_len))
            ret = UTRC_RX_ERROR.LEN
        elif rx_utrc.rw != tx_utrc.rw:
            print("[UtrcCli] Error: UTRC_RX_ERROR.RW: %d %d" % (rx_utrc.rw, tx_utrc.rw))
            ret = UTRC_RX_ERROR.RW
        elif rx_utrc.cmd != tx_utrc.cmd:
            print("[UtrcCli] Error: UTRC_RX_ERROR.CMD: %d %d" % (rx_utrc.cmd, tx_utrc.cmd))
            ret = UTRC_RX_ERROR.CMD

        return (ret, rx_utrc)


class UX2HEX_RXSTART:
    FROMID = 0
    TOID = 1
    LEN = 2
    DATA = 3
    CRC1 = 4
    CRC2 = 5
    RXLEN_MAX = 64


class UtrcDecode:
    def __init__(self, fromid, toid):
        self.DB_FLG = "[ux2 ptcl] "
        self.rxstate = UX2HEX_RXSTART.FROMID
        self.data_idx = 0
        self.len = 0
        self.fromid = fromid
        self.toid = toid

    # wipe cache , set from_id and to_id
    def flush(self, fromid=-1, toid=-1):
        self.rxstate = UX2HEX_RXSTART.FROMID
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
            if UX2HEX_RXSTART.FROMID == self.rxstate:
                if self.fromid == rxch[0] or self.fromid == 0x55:
                    self.rxbuf = rxch
                    self.rxstate = UX2HEX_RXSTART.TOID

            elif UX2HEX_RXSTART.TOID == self.rxstate:
                if self.toid == rxch[0]:
                    self.rxbuf += rxch
                    self.rxstate = UX2HEX_RXSTART.LEN
                else:
                    self.rxstate = UX2HEX_RXSTART.FROMID

            elif UX2HEX_RXSTART.LEN == self.rxstate:
                if (rxch[0] & 0x7F) < UX2HEX_RXSTART.RXLEN_MAX:
                    self.rxbuf += rxch
                    self.len = rxch[0] & 0x7F
                    self.data_idx = 0
                    self.rxstate = UX2HEX_RXSTART.DATA
                else:
                    self.rxstate = UX2HEX_RXSTART.FROMID

            elif UX2HEX_RXSTART.DATA == self.rxstate:
                if self.data_idx < self.len:
                    self.rxbuf += rxch
                    self.data_idx += 1
                    if self.data_idx == self.len:
                        self.rxstate = UX2HEX_RXSTART.CRC1
                else:
                    self.rxstate = UX2HEX_RXSTART.FROMID

            elif UX2HEX_RXSTART.CRC1 == self.rxstate:
                self.rxbuf += rxch
                self.rxstate = UX2HEX_RXSTART.CRC2

            elif UX2HEX_RXSTART.CRC2 == self.rxstate:
                self.rxbuf += rxch
                self.rxstate = UX2HEX_RXSTART.FROMID
                crc = crc16.crc_modbus(self.rxbuf[:self.len + 3])
                if crc[0] == self.rxbuf[self.len + 3] and crc[1] == self.rxbuf[self.len + 4]:
                    if rx_que.full():
                        rx_que.get()
                    rx_que.put(self.rxbuf)
                    # print_msg.nhex("[SockSeri] rx_que.put: ", self.rxbuf, len(self.rxbuf))
