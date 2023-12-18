import Abacus as aba
import random
import unittest

abacus = aba.Abacus()
human = aba.Human(abacus)


class MyTestCase(unittest.TestCase):

    def test_load(self):
        numb = random.randint(0, 191102975)
        abacus.load(numb)
        self.assertEqual(numb, int(abacus))  # add assertion here

    def test_mult(self):
        a, b = (random.randint(0, 13824) for _ in range(2))
        human.multiplication(a, b)
        self.assertEqual(a * b, int(abacus))

    def test_div(self):
        a, b = (random.randint(0, 13824) for _ in range(2))
        if b > a: a, b = b, a
        abacus.load(a)
        reminder = human.div1(b)
        abacus.clear(start=reminder)
        self.assertEqual(a // b, int(abacus))


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