import Abacus as Aba
import argparse

def table_num_listise(table='abacus.csv'):
    call = open(table, 'r+')
    call = call.readlines()
    call = [pl.split(',') for pl in call]
    """
    for i in call:
        i = [pl == '•' for pl in i]
    """
    back = []
    for line in call:
        up = False
        high = False
        i, j = 0, 0
        for pl in line:
            if pl == '---':
                up = True
            if pl == '-||':
                high = True
                up = False
            if pl == '-O-' and up:
                if not high:
                    i += 1
                else:
                    j += 1
        back += (i, j)
    return back


def decimate(call: list[int]):
    # input: number list
    back = 0
    for pl, num in enumerate(call):
        row = pl // 2
        high = pl % 2
        back += num * 24 ** row * 6 ** high
    return back



if __name__ == "__main__":
    file = 'abacus.csv'
    abacus = Aba.Abacus()
    try:
        abacus.num_read(table_num_listise(file))
    except FileNotFoundError:
        abacus.clear()
    parser = argparse.ArgumentParser()
    parser.add_argument('--clear', help=abacus.clear.__doc__, action="store_true")
    args = parser.parse_args()
    if args.clear:
        abacus.clear()

    abacus.prnt(tee=True)
    """
    num = table_num_listise()
    print(num)   
    print(decimate(num))
    """