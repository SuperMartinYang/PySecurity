class MyAES:
    """
    4 steps:
        1. byte exchange
        2. row shift
        3. col mix
        4. encrypt with key         <=== key generate
    Usage:
        AES-128   10 ROUNDS
        plaintext: 0x0123456789abcdef0123456789abcdef
        key: 0x0123456789abcdef0123456789abcdef
        ciphertext: 0x.........................
        AES-192   12 ROUNDS
        AES-256   14 ROUNDS
    """
    def encrypt(self):
        """

        :return:
        """

    def decrypt(self):
        """

        :return:
        """
