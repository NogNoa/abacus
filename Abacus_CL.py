import Abacus as Aba
import argparse
from string import ascii_lowercase


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


def decimate(call: list):
    # input: number list
    back = 0
    for pl, num in enumerate(call):
        row = pl // 2
        high = pl % 2
        back += num * 24 ** row * 6 ** high
    return back


def base24_decimise(call: str):
    call = call.lower()
    base = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] + list(ascii_lowercase[:14])
    back = 0
    for pl, digit in enumerate(call[::-1]):
        digit = base.index(digit)
        back += digit * 24 ** pl
    return back


def color_cellise(color: str):
    color = color.lower()
    colori = ['red', 'yellow', 'green', 'blue', 'indigo', "violet"]
    return 2 * colori.index(color)

def decide_base(call):
    if decimal:
        value = int(call)
    else:
        value = base24_decimise(call)
    return value

if __name__ == "__main__":
    file = 'abacus.csv'
    abacus = Aba.Abacus()
    decimal = False
    try:
        abacus.num_read(table_num_listise(file))
    except FileNotFoundError:
        abacus.clear()
    parser = argparse.ArgumentParser(description=Aba.help_dscrpt)
    parser.add_argument('-v', '--verbose', help="Make me announce more stuff", action="store_true")
    parser.add_argument('-d', '--decimal', help="This means you wish to enter in base10 instead", action="store_true")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument('--up', help=abacus.right.__doc__, action="count")
    actions.add_argument('--down', help=abacus.left.__doc__, action="count")
    actions.add_argument('--clear', help=Aba.Cell.clear.__doc__)
    actions.add_argument('--set', help=Aba.Cell.set.__doc__)
    actions.add_argument('--add', help=abacus.add1.__doc__, nargs=2)
    actions.add_argument('--sub', help=abacus.sub1.__doc__, nargs=2)
    actions.add_argument('--multi', help=abacus.mult1.__doc__, nargs=2)
    actions.add_argument('--load', help=Aba.Cell.load.__doc__, nargs=2)
    actions.add_argument('--push', help=Aba.Cell.push.__doc__, nargs=2)
    actions.add_argument('--pull', help=Aba.Cell.pull.__doc__, nargs=2)
    actions.add_argument('--clear_full', help=abacus.clear.__doc__, action="store_true")
    actions.add_argument('--load_full', help=abacus.load.__doc__)

    args = parser.parse_args()
    if args.verbose:
        Aba.verbose = True
    if args.decimal:
        decimal = True
    if args.clear_full:
        abacus.clear()
    if args.load_full is not None:
        value = decide_base(args.load_full)
        abacus.load(value)
    if args.up:
        for i in range(args.up):
            abacus.right()
    if args.down:
        for i in range(args.down):
            abacus.left()
    if args.clear is not None:
        cell = color_cellise(args.clear)
        abacus.val[cell].clear()
        abacus.val[cell + 1].clear()
    if args.set is not None:
        cell = color_cellise(args.set)
        abacus.val[cell].set()
        abacus.val[cell + 1].set()

    if args.load is not None:
        call = args.load
        cell = color_cellise(call[1])
        value = decide_base(call[0])
        abacus.val[cell].load(value, True)
    if args.push is not None:
        call = args.push
        cell = color_cellise(call[1])
        force = base24_decimise(call[0])
        abacus.val[cell].push(force)
    if args.pull is not None:
        call = args.pull
        cell = color_cellise(call[1])
        force = base24_decimise(call[0])
        abacus.val[cell].pull(force)

    if args.add is not None:
        value = decide_base(args.add)
        abacus.add1(value)
    if args.sub is not None:
        value = decide_base(args.sub)
        abacus.sub1(value)
    if args.multi is not None:
        value = decide_base(args.multi)
        abacus.mult1(value)

    abacus.prnt(tee=not Aba.verbose)
    if Aba.verbose:
        print("FIN")
    """
    num = table_num_listise()
    print(num)   
    print(decimate(num))
    """

"""DONE:base24 input.
Color to cell"""
