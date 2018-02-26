import codecs

from Security.Cryptography.BitManipulation import BitManipulations
from Security.Cryptography.bytes_hex_int import MyBHIconvertor


class MySHA256:
    """
    4 steps:
        1. add padding
        2. add length info
        3. init buffer
        4. separate and deal
    """
    # Constant Table
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ]
    # init hash value
    H = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

    # Manipulate bits, bytes...
    BM = BitManipulations()
    MBC = MyBHIconvertor()

    # logical functions
    @staticmethod
    def CH(x, y, z):
        return (x & y) ^ ((~ x) & z)

    @staticmethod
    def MAJ(x, y, z):
        return (x & y) ^ (x & z) ^ (y & z)

    @staticmethod
    def BSIG0(x):
        return MySHA256.BM.rotr(x, 2) ^ MySHA256.BM.rotr(x, 13) ^ MySHA256.BM.rotr(x, 22)

    @staticmethod
    def BSIG1(x):
        return MySHA256.BM.rotr(x, 6) ^ MySHA256.BM.rotr(x, 11) ^ MySHA256.BM.rotr(x, 25)

    @staticmethod
    def SSIG0(x):
        return MySHA256.BM.rotr(x, 7) ^ MySHA256.BM.rotr(x, 18) ^ MySHA256.BM.shr(x, 3)

    @staticmethod
    def SSIG1(x):
        return MySHA256.BM.rotr(x, 17) ^ MySHA256.BM.rotr(x, 19) ^ MySHA256.BM.shr(x, 10)

    def addPadding(self, msg):
        """
        k is len(msg)
        1 is one 1 bit
        L is number of zero added
        k + 1 + L mod 512 = 448
        :param msg: byte str
        :return:
        """
        msgLen = len(msg)
        msg += b'\x80'
        blocksNum = (msgLen + 1 + 8 + (64 - 1)) // 64
        required_len = blocksNum * 64
        paddingLen = required_len - msgLen - 1 - 8

        # Append the 0's padding
        msg += paddingLen * b"\x00"
        msg += codecs.decode("%016X" % (msgLen * 8), 'hex_codec')   # msg bits -> bytes stream of 64 bits represents

        return msg

    def separate(self, msg):
        """
        separate msg into blocks of 512-bit
        :param self:
        :return: list
        """
        blocks = []
        for i in range(0, len(msg), 64):
            blocks.append(msg[i: i + 64])
        return blocks

    def deal(self, block):
        """
        combine all func together
        :param block:
        :return:
        """
        w = []
        # init for one block
        for i in range(0, len(block), 4):
            w.append(self.MBC.bytes2int(block[i: i + 4], 'big'))
        for i in range(16, 64):
            w.append((self.SSIG1(w[i - 2]) + w[i - 7] + self.SSIG0(w[i - 15]) + w[i - 16]) & 0xffffffff)
        a = self.H[0]
        b = self.H[1]
        c = self.H[2]
        d = self.H[3]
        e = self.H[4]
        f = self.H[5]
        g = self.H[6]
        h = self.H[7]

        for i in range(64):
            t1 = (h + self.BSIG1(e) + self.CH(e, f, g) + self.K[i] + w[i]) & 0xffffffff
            t2 = (self.BSIG0(a) + self.MAJ(a, b, c)) & 0xffffffff
            h = g
            g = f
            f = e
            e = (d + t1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xffffffff

        self.H[0] += a
        self.H[1] += b
        self.H[2] += c
        self.H[3] += d
        self.H[4] += e
        self.H[5] += f
        self.H[6] += g
        self.H[7] += h

        for j in range(len(self.H)):
            self.H[j] = self.H[j] & 0xFFFFFFFF

    def digest(self, msg, options):
        """

        :param msg:
        :param options: str, bytes str, hex-bytes
        :return:
        """
        res = b''
        if options == 'hex-bytes':
            msg = self.MBC.hex2bytes(msg)
        elif options == 'string':
            msg = self.MBC.str2bytes(msg, "ascii")
        msg = self.addPadding(msg)
        blocks = self.separate(msg)
        for block in blocks:
            self.deal(block)
        for h in self.H:
            res += self.MBC.int2bytes(h, 'big')
        return res

sha = MySHA256()
mb = MyBHIconvertor()
print(mb.bytes2hex(sha.digest("abcd", "string"), 'big'))
