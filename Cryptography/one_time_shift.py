class OneTimeShift(object):
    def knownPlainCipher(self, ciphertext, plaintext):
        """
        given plain text and cipher text
        find the key string
        :param self:
        :param plaintext:
        :param ciphertext:
        :return:
        """
        KeySpace = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
        keyStream = ''
        for index in range(len(plaintext)):
            keyStream += KeySpace[(ord(ciphertext[index]) - ord(plaintext[index])) % 27]

        return keyStream

one = OneTimeShift()
print(one.knownPlainCipher("ANKYODKYUREPFJBYOJDSPLREYIUNOFDOIUERFPLUYTS", "MR MUSTARD WITH THE CANDLESTICK IN THE HALL"))
print(one.knownPlainCipher("ANKYODKYUREPFJBYOJDSPLREYIUNOFDOIUERFPLUYTS", "MISS SCARLET WITH THE KNIFE IN THE LIBRARY "))
print(one.knownPlainCipher("ANKYODKYUREPFJBYOJDSPLREYIUNOFDOIUERFPLUYTS", "MEET ME ON FRIDAY AT SIX PM                "))
