import math

import Abacus as aba
import random
import unittest

P24_3 = 13823
P24_5 = 7962623
P24_6 = 191102975


class CellTestCase(unittest.TestCase):
    def setUp(self):
        self.id = 'r0'
        self.earth = aba.Cell('earth', 0, self.id)  # lower cell
        self.sky = aba.Cell('sky', 1, self.id)  # upper cell


class RodTestCase(unittest.TestCase):
    def setUp(self):
        self.rod = aba.Rod(0, 'red')

    def test_push_0(self):
        a = random.randint(0, 24)
        self.rod.push(a)
        self.assertEqual(a, int(self.rod))

    def test_exchange(self):
        other_rod = aba.Rod(1, 'yellow')
        a = random.randint(0, 24)
        b = random.randint(0, 24 - a)
        self.rod.push(a)
        other_rod.push(b)
        aba.exchange(self.rod, other_rod)
        self.assertFalse(int(self.rod))
        self.assertEqual(a + b, int(other_rod))

    def test_exchange_0(self):
        other_rod = aba.Rod(1, 'yellow')
        a = random.randint(0, 24)
        self.rod.push(a)
        aba.exchange(self.rod, other_rod)
        self.assertFalse(int(self.rod))
        self.assertEqual(a, int(other_rod))


class AbacusTestCase(unittest.TestCase):

    def setUp(self):
        self.abacus = aba.Abacus()

    def test_clear(self):
        numb = random.randint(0, P24_6)
        self.abacus._fast_load(numb)
        self.abacus.clear()
        self.assertEqual(0, int(self.abacus))

    def test_clear_pos(self):
        numb = random.randint(0, P24_6)
        rod = random.randint(1, 6)
        factor = 24 ** rod
        self.abacus._fast_load(numb)
        self.abacus.clear(rod_0=rod)
        self.assertEqual(numb % factor, int(self.abacus))

    def test_set(self):
        numb = random.randint(0, P24_6)
        self.abacus._fast_load(numb)
        self.abacus.set()
        self.assertEqual(P24_6, int(self.abacus))

    def test_push(self):
        numb = random.randint(0, P24_6)
        self.abacus._fast_load(numb)
        a =  random.randint(0, P24_6 - numb)
        self.abacus.push(0, a)
        self.assertEqual(numb + a, int(self.abacus))

    def test_push_0(self):
        numb = random.randint(0, P24_6)
        self.abacus.push(0, numb)
        self.assertEqual(numb, int(self.abacus))

    def test_push_pos(self):
        numb = random.randint(0, P24_6)
        self.abacus._fast_load(numb)
        a =  random.randint(0, 24)
        rod = random.randint(0, 5)
        self.abacus.push(rod, a)
        self.assertEqual(numb + a * 24 ** rod, int(self.abacus))

    def test_push_pos_carry(self):
        numb = random.randint(0, P24_6)
        self.abacus._fast_load(numb)
        rod = random.randint(0, 5)
        a =  random.randint(24 - int(self.abacus.val[rod]), 48)
        self.abacus.push(rod, a)
        self.assertEqual(numb + a * 24 ** rod, int(self.abacus))

    def test_load(self):
        numb = random.randint(0, P24_6)
        self.abacus.load(numb)
        self.assertEqual(numb, int(self.abacus))

    def test_magnitude(self):
        numb = random.randint(0, P24_6)
        self.abacus._fast_load(numb)
        expected = math.ceil(math.log(numb, 24))
        self.assertEqual(expected, self.abacus.magnitude())

    def test_right(self):
        numb = random.randint(0, P24_6)
        self.abacus._fast_load(numb)
        rem = self.abacus.right()
        result = int(self.abacus)
        self.assertEqual(numb // 24, result)
        self.assertEqual(numb / 24, result + rem / 24)

    def test_left(self):
        numb = random.randint(0, P24_6)
        self.abacus._fast_load(numb)
        rem = self.abacus.left()
        result = int(self.abacus)
        self.assertEqual(numb * 24 % (P24_6 + 1), result)
        self.assertEqual(numb * 24, result + rem * (P24_6 + 1))

    def test_num_print_top(self):
        numb = random.randint(0, P24_6)
        rod = random.randint(1, 6)  # the zero case is in almost every test here
        self.abacus._fast_load(numb)
        for _ in range(rod):
            numb //= 24
        self.assertEqual(numb, self.abacus.num_print(rod, 6))

    def test_num_print_bottom(self):
        numb = random.randint(0, P24_6)
        rod = random.randint(0, 6)
        self.abacus._fast_load(numb)
        numb %= (24 ** rod)
        self.assertEqual(numb, self.abacus.num_print(rod))


class HumanTestCase(unittest.TestCase):

    def setUp(self):
        self.abacus = aba.Abacus()
        self.human = aba.Human(self.abacus)

    def test_add(self):
        a, b = (random.randint(0, P24_6) for _ in range(2))
        if b > a: a, b = b, a
        self.abacus._fast_load(a)
        self.human.add1(b)
        self.assertEqual((a + b) % (P24_6 + 1), int(self.abacus))

    def test_sub(self):
        a, b = (random.randint(0, P24_6) for _ in range(2))
        if b > a: a, b = b, a
        self.abacus._fast_load(a)
        self.human.sub1(b)
        self.assertEqual(a - b, int(self.abacus))

    def test_mult2(self):
        length = random.choice((0, 1, 1, 2, 2, 2))
        a = random.randint(0, 24 ** length)
        b = random.randint(0, 24 ** (4 - length))
        self.human.multiplication(a, b)
        self.assertEqual(a * b, int(self.abacus))

    def test_mult1(self):
        length = random.choice((0, 1, 1, 2, 2, 2))
        a = random.randint(0, 24 ** length)
        b = random.randint(0, 24 ** (4 - length))
        self.abacus._fast_load(a)
        self.human.mult1(b)
        self.assertEqual(a * b, int(self.abacus))

    def test_div(self):
        divisor = random.randint(1, P24_5)
        lngth_sor = math.ceil(math.log(divisor, 24))
        dividand = random.randint(divisor, min(int(24 ** (5 + lngth_sor) / 2), P24_5))

        self.abacus._fast_load(dividand)
        reminder_p = self.human.div1(divisor)
        reminder = self.abacus.num_print(reminder_p, 6)
        self.abacus.clear(rod_0=reminder_p)
        self.assertEqual(dividand // divisor, int(self.abacus))
        self.assertEqual(dividand % divisor, reminder)


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
