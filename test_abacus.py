import Abacus as aba

verbose = aba.verbose = True
abacus = aba.Abacus()
# abacus.multiplication(24 ** 2, 24 ** 4 - 1)
# abacus.num_read([4 + 2*6, 0, 23, 23, 23, 5 + 6])
# print(int(abacus))
abacus.load(2 * 24)
abacus.subfrom1(12 * 24 ** 2)
# abacus.div1(2)
abacus.prnt(tee=not verbose)
if verbose:
    print("FIN")