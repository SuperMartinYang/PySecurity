from Cryptodome.Cipher import DES
class MyDES:
    """
    Usage:
        input: 0x0123456789ABCDEF
        key: 0x133457799BBCDFF1
        output: 0x8444a39a8f7817cf
    """
    def str2bits(self, text, length):
        # text = int.from_bytes(bytes(text, "latin-1"), "little")
        text = int(text, 16)
        text = bin(text)
        # bitArray = [0 for _ in range(length)]
        # for i in range(length):
        #     if i % 4 == 0:
        #         cnt = 3
        #         bitArray[i + cnt] = text & 0x1
        #     else:
        #         cnt -= 2
        #         bitArray[i + cnt] = text & 0x1
        #     text >>= 1
        i = 0
        bitArray = [0 for _ in range(length)]
        while i < len(text) - 2:
            bitArray[length - 1 - i] = int(text[len(text) - i - 1])
            i += 1
        return bitArray

    def bytes2bits(self, text, length):
        bitArray = [0 for _ in range(length)]
        for i in range(length):
            if i % 4 == 0:
                cnt = 3
                bitArray[i + cnt] = text & 0x1
            else:
                cnt -= 2
                bitArray[i + cnt] = text & 0x1
            text >>= 1
        return bitArray

    def bits2str(self, bitArray):
        text = [str(i) for i in bitArray]
        text = int(''.join(text),2)
        # for i in range(len(bitArray)):
        #     if i % 4 == 0:
        #         cnt = 3
        #         text |= bitArray[i] << (i + cnt)
        #     else:
        #         cnt -= 2
        #         text |= bitArray[i] << (i + cnt)
        return hex(text)

    def keygenerate(self, key, seq=0, forward = True):
        """
        generate key
        :return: list[] 0 -> n - 1
        """
        pc1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
        pc2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
        shiftTable = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        realKey = [0 for _ in range(56)]
        for i in range(len(pc1)):
            realKey[i] = key[pc1[i] - 1]
        shiftNum = sum(shiftTable[:seq + 1]) if forward else sum(shiftTable[:len(shiftTable) - seq])
        shiftNum %= 28
        # leftpart & rightpart
        leftShifted = realKey[0:shiftNum]
        rightShifted = realKey[28:28 + shiftNum]
        for i in range(28):
            if i + shiftNum > 27:
                continue
            else:
                realKey[i] = realKey[i + shiftNum]
                realKey[i + 28] = realKey[i + shiftNum + 28]
        for i in range(28 - shiftNum, 28):
            realKey[i] = leftShifted[i - 28 + shiftNum]
            realKey[i + 28] = rightShifted[i - 28 + shiftNum]
        finalKey = [0 for _ in range(48)]
        for i in range(len(pc2)):
            finalKey[i] = realKey[pc2[i] - 1]
        return finalKey

    def expand(self, ri):
        """

        :param ri: list[]
        :return: list[]
        """
        expandTable = [
            32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11,
            12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21,
            22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
        ]
        # ri = self.str2bits(ri, 32)
        res = [0 for _ in range(len(expandTable))]
        for i in range(len(expandTable)):
            res[i] = ri[expandTable[i] - 1]

        return res

    def permutation(self, text, choice=0):
        """
        choice: 0-> ip, 1-> ip inverse, 2 -> pbox for shrink
        :param text: list
        :param choice: int
        :return: list
        """
        ip = [
            58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
        ]
        iIp = [
            40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
        ]
        pbox = [
            16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
            2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25
        ]
        tmpIp = iIp if choice == 1 else ip if choice == 0 else pbox
        # text = self.str2bits(text, len(tmpIp))
        res = [0 for _ in range(len(tmpIp))]
        for i in range(len(tmpIp)):
            res[i] = text[tmpIp[i] - 1]

        return res

    def f(self, ri, ki1):
        """

        :param ri: list
        :param ki1: list
        :return: list
        """
        rix = self.expand(ri)
        tmp = [rix[i] ^ ki1[i] for i in range(len(rix))]
        shrink = self.sbox(tmp)
        return self.permutation(shrink, 2)

    def sbox(self, tmp):
        S_Box = [
            [  # s1
                14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
                0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
                4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
                15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13,
            ],
            [  # s2
                15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
                3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
                0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
                13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9,
            ],
            [  # s3
                10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
                13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
                13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
                1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12,
            ],
            [  # s4
                7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
                13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
                10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
                3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14,
            ],
            [  # s5
                2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
                14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
                4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
                11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3,
            ],
            [  # s6
                12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
                10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
                9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
                4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13,
            ],
            [  # s7
                4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
                13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
                1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
                6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12,
            ],
            [  # s8
                13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
                1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
                7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
                2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11
            ]
        ]
        res = []
        for i in range(0, len(tmp), 6):
            item = i // 6
            row = tmp[i] << 1 | tmp[i + 5]
            col = tmp[i + 4] | tmp[i + 3] << 1 | tmp[i + 2] << 2 | tmp[i + 1] << 3
            val = S_Box[item][row * 16 + col]
            res.extend(self.bytes2bits(val, 4))
        return res

    def encrypt(self, plaintext, key):
        plaintext = self.str2bits(plaintext, 64)
        plaintext = self.permutation(plaintext, 0)
        key = self.str2bits(key, 64)
        l0 = plaintext[:32]
        r0 = plaintext[32:]
        for i in range(16):
            k1 = self.keygenerate(key, i)
            r1Half = self.f(r0, k1)
            tmpR0 = r0
            r0 = [l0[i] ^ r1Half[i] for i in range(32)]
            l0 = tmpR0
        r0.extend(l0)
        ciphertext = self.permutation(r0, 1)
        return self.bits2str(ciphertext)

    def decrypt(self, ciphertext, key):
        ciphertext = self.str2bits(ciphertext, 64)
        ciphertext = self.permutation(ciphertext, 0)
        key = self.str2bits(key, 64)
        l0 = ciphertext[:32]
        r0 = ciphertext[32:]
        for i in range(16):
            k1 = self.keygenerate(key, i, forward=False)
            tmpR0 = r0
            r1Half = self.f(r0, k1)
            r0 = [l0[i] ^ r1Half[i] for i in range(32)]
            l0 = tmpR0
        r0.extend(l0)
        plaintext = self.permutation(r0, 1)
        return self.bits2str(plaintext)


tryDes = MyDES()
# plaintext = b"\x10\x32\x54\x76\x98\xba\xdc\xfe"
plaintext = input("Please input the plaintext (Hex str): ")
key = input("Please input the key (Hex str): ")
ciphertext = tryDes.encrypt(plaintext, key)
print(ciphertext)
plaintext2 = tryDes.decrypt(ciphertext, key)
print(plaintext2)
# key = bytes(key, 'latin-1')
# plaintextBytes = bytes(plaintext, 'latin-1')
# des = DES.new(key, DES.MODE_ECB)
# print(hex(int.from_bytes(des.encrypt(plaintextBytes), "little")))
