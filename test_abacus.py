import Abacus as aba

verbose = aba.verbose = True
abacus = aba.Abacus()
human = aba.Human(abacus)
# human.multiplication(24 ** 2, 24 ** 4 - 1)
# abacus.num_read([4 + 2*6, 0, 23, 23, 23, 5 + 6])
# print(int(abacus))
abacus.load(2 * 24)
human.subfrom1(12 * 24 ** 2)
# human.div1(2)
abacus.prnt(tee=not verbose)
if verbose:
    print("FIN")