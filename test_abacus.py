import math

import Abacus as aba
import random
import unittest

abacus = aba.Abacus()
human = aba.Human(abacus)

P24_3 = 13823
P24_5 = 7962623
P24_6 = 191102975


class MyTestCase(unittest.TestCase):

    def test_load(self):
        numb = random.randint(0, P24_6)
        abacus.load(numb)
        self.assertEqual(numb, int(abacus))

    def test_magnitude(self):
        numb = random.randint(0, P24_6)
        abacus._fast_load(numb)
        expected = math.ceil(math.log(numb, 24))
        self.assertEqual(expected, abacus.magnitude())

    def test_right(self):
        numb = random.randint(0, P24_6)
        abacus._fast_load(numb)
        rem = abacus.right()
        result = int(abacus)
        self.assertEqual(numb // 24, result)
        self.assertEqual(numb / 24, result + rem / 24)

    def test_left(self):
        numb = random.randint(0, P24_6)
        abacus._fast_load(numb)
        rem = abacus.left()
        result = int(abacus)
        self.assertEqual(numb * 24 % (P24_6 + 1), result)
        self.assertEqual(numb * 24, result + rem * (P24_6 + 1))

    def test_add(self):
        a, b = (random.randint(0, P24_6) for _ in range(2))
        if b > a: a, b = b, a
        abacus._fast_load(a)
        human.add1(b)
        self.assertEqual((a + b) % (P24_6 + 1), int(abacus))

    def test_sub(self):
        a, b = (random.randint(0, P24_6) for _ in range(2))
        if b > a: a, b = b, a
        abacus._fast_load(a)
        human.sub1(b)
        self.assertEqual(a - b, int(abacus))

    def test_mult(self):
        length = random.choice((0, 1, 1, 2, 2, 2))
        a = random.randint(0, 24 ** length)
        b = random.randint(0, 24 ** (4 - length))
        human.multiplication(a, b)
        self.assertEqual(a * b, int(abacus))

    def test_div(self):
        divisor = random.randint(1, P24_5)
        lngth_sor = math.ceil(math.log(divisor, 24))
        dividand = random.randint(divisor, min(int(24 ** (5 + lngth_sor) / 2), P24_5))

        abacus._fast_load(dividand)
        reminder = human.div1(divisor)
        abacus.clear(start=reminder)
        self.assertEqual(dividand // divisor, int(abacus))


if __name__ == '__main__':
    unittest.main()
# verbose = aba.verbose = True

# # human.multiplication(24 ** 2, 24 ** 4 - 1)
# # abacus.num_read([4 + 2*6, 0, 23, 23, 23, 5 + 6])
# # print(int(abacus))
# abacus.load(2 * 24)
# human.subfrom1(12 * 24 ** 2)
# # human.div1(2)
# abacus.prnt(tee=not verbose)
# if verbose:
#     print("FIN")
