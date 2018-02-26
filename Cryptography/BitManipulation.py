# This is used in bitwise rotate, rotr, rotl
class BitManipulations:
    # only used for 32-bit integer
    def rotr(self, bitVal, rotNum):
        """
        Rotate right, bitVal -> rotNum position
        :param bitVal: int
        :param rotNum: int
        :return: int
        """
        return ((bitVal >> rotNum) | (bitVal << (32 - rotNum))) & 0xffffffff

    def rotl(self, bitVal, rotNum):
        """
        rotate left
        :param bitVal:
        :param rotNum:
        :return:
        """
        return ((bitVal << rotNum) | (bitVal >> (32 - rotNum))) & 0xffffffff

    def shr(self, bitVal, shiftNum):
        """
        shift logical right, bitVal
        :param bitVal:
        :param shiftNum:
        :return:
        """
        return bitVal >> shiftNum

    def shl(self, bitVal, shiftNum):
        """
        shift logical left, bitVal
        :param bitVal:
        :param shiftNum:
        :return:
        """
        return (bitVal << shiftNum) & 0xffffffff

    def sar(self, bitVal, shiftNum):
        """
        shift arithmetic right, bitVal
        :param bitVal:
        :param shiftNum:
        :return:
        """

    def sal(self, bitVal, shiftNum):
        """
        shift arithmetic left, bitVal
        :param bitVal:
        :param shiftNum:
        :return:
        """
    def getBit(self, bitVal, position):
        """
        get the bit in position
        :param bitVal:
        :param position:
        :return:
        """

    def setBack(self, bitVal, position, tag):
        """
        set bits after position to be zero or one
        :param bitVal: int
        :param position: int
        :param tag: 0 / 1
        :return: int
        """

    def setFront(self, bitVal, position, tag):
        """
        set bits from position to the most significant bit to be zero or one
        :param bitVal:
        :param position:
        :param tag: 0 / 1
        :return:
        """