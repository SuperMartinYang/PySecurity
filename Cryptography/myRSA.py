import math
class MyRSA:
    @staticmethod
    def egcd(b, a):
        """
        ax + by = g = gcd(x,y)
        :param a: x
        :param b: y
        :return: [g, a, b]
        """
        x0, x1, y0, y1 = 1, 0, 0, 1
        while a != 0:
            q, b, a = b // a, a, b % a
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        return b, x0, y0

    def get_a(self, p, q, b):
        """
        n = pq
        theta(n) = (p-1)(q-1)
        gcd(b, n) = 1
        egcd(b, n) = a
        :param p:
        :param q:
        :param b:
        :return:
        """
        theta = (p - 1) * (q - 1)
        inverse = MyRSA.egcd(b, theta)[1]
        return inverse if inverse > 0 else inverse + theta

    def SQM(self, x, b, n):
        """
        get the answer of x^b mod n
        :param n: mod
        :param x: bot
        :param b: exponent
        :return: answer
        """
        u = 1
        k = int(math.log2(b))

        for i in range(k, -1, -1):
            u = (u * u) % n;
            if b & (1 << i) == (1 << i):
                u = (u * x) % n;
        return u

    def CRT(self, y, a, p, q, n):
        """
        x = y^a mod n
        :param y: cipher text
        :param a: private key int
        :param p: prime 2
        :param q: prime 1
        :param b: random number
        :param n: pq
        :return: plain text int
        """
        ap = a % (p - 1)
        aq = a % (q - 1)
        M1 = q
        M2 = p
        tmp = self.egcd(M1, p)[1]
        up = tmp if tmp > 0 else tmp + p
        tmp = self.egcd(M2, q)[1]
        uq = tmp if tmp > 0 else tmp + q
        yp = y % p
        yq = y % q
        xp = self.SQM(yp, ap, p)
        xq = self.SQM(yq, aq, q)

        return (xp * up * q + xq * uq * p) % n

    def fake_decrypt(self, y, n, p, q, b):
        def change2word(x):
            res = ''
            while x > 0:
                res = chr(x % 26 + 0x41) + res
                x //= 26
            return res

        a = self.get_a(p, q, b)
        # x = y^a mod n
        x = self.CRT(y, a, p, q, n)
        return change2word(x)

rsa = MyRSA()
print(rsa.fake_decrypt(12423, 18923, 127, 149, 1261))