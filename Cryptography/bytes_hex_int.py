import struct


class MyBHIconvertor:
    @staticmethod
    def bytes2int(byteStr, byteorder):
        return int.from_bytes(byteStr, byteorder)

    @staticmethod
    def int2bytes(i, byteorder):
        if byteorder == 'big':
            fmt = '>I'
        else:
            fmt = '<H'
        return struct.pack(fmt, i)

    @staticmethod
    def int2hex(i):
        return hex(i)

    @staticmethod
    def hex2int(h):
        if len(h) > 1 and h[0:2] == '0x':
            h = h[2:]

        if len(h) % 2:
            h = "0" + h

        return int(h, 16)

    @staticmethod
    def hex2bytes(h):
        if len(h) > 1 and h[0:2] == '0x':
            h = h[2:]

        if len(h) % 2:
            h = "0" + h
        return bytes.fromhex(h)

    def bytes2hex(self, byteStr, byteorder):
        return hex(self.bytes2int(byteStr, byteorder))

    @staticmethod
    def str2bytes(s, encoding):
        return s.encode(encoding)

    @staticmethod
    def bytes2str(byteStr, encoding):
        return byteStr.decode(encoding)
