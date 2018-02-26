import random


def hex2raw(hexList):
    res = ''
    for i in hexList:
        res += chr(int(i, 16))
    return res


def formHexListFromFile(filename):
    with open(filename, 'r') as hexFile:
        hexString = hexFile.read()
        hexList = hexString.split()
        res = hex2raw(hexList)
    return res


def appendJunk(res):
    for i in range(40):
        res += chr(int(random.random() * 26) + 0x40)
    return res


filename = input()
print(appendJunk(formHexListFromFile(filename)))
