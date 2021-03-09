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
        rod = pl // 2
        high = pl % 2
        back += num * 24 ** rod * 6 ** high
    return back


def icositetrise(call: list):
    # input: number list
    base = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] + list(ascii_lowercase[:14])
    back = ''
    for pl, num in enumerate(call):
        if not pl % 2:
            dec = num
        else:
            dec += num * 6
            char = base[dec]
            back = char + back
    return back


def base24_decimise(call: str):
    call = call.lower()
    base = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] + list(ascii_lowercase[:14])
    back = 0
    for pl, digit in enumerate(call[::-1]):
        try:
            digit = base.index(digit)
        except ValueError:
            print(f"Oops, \"{call}\" is not a base24 number")
            exit(2)
        back += digit * 24 ** pl
    return back


def color_cellise(color: str):
    colori = {c.color.lower(): c.pl for c in abacus.val[::2]}
    try:
        return colori[color.lower()]
    except KeyError:
        print(f"Oops, \"{color}\" is not a color in this abacus")
        exit(3)


def decide_base(call):
    if decimal:
        try:
            return int(call)
        except ValueError:
            print(f"Oops, \"{call}\" is not a decimal number")
            exit(1)
    else:
        return base24_decimise(call)


def call_parse(call):
    value, cell = call
    cell = color_cellise(cell)
    value = decide_base(value)
    return value, cell


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
    actions.add_argument('--clear_full', help=abacus.clear.__doc__, action="store_true")
    actions.add_argument('--set', help=Aba.Cell.set.__doc__)
    actions.add_argument('--add', help=abacus.add1.__doc__)
    actions.add_argument('--sub', '--subtract', help=abacus.sub1.__doc__)
    actions.add_argument('--sub_from', '--subtract_from', help=abacus.subfrom1.__doc__)
    actions.add_argument('--multi', '--multiply', help=abacus.mult1.__doc__)
    actions.add_argument('--div', '--divide', help=abacus.div1.__doc__)
    actions.add_argument('--load', help=Aba.Cell.load.__doc__, nargs=2)
    actions.add_argument('--load_full', help=abacus.load.__doc__)
    actions.add_argument('--push', help=Aba.Cell.push.__doc__, nargs=2)
    actions.add_argument('--pull', help=Aba.Cell.pull.__doc__, nargs=2)
    actions.add_argument('--ico', '--icositetrise', help=icositetrise.__doc__, action="store_true")

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
        for count in range(args.up):
            abacus.right()
    if args.down:
        for count in range(args.down):
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
        value, cell = call_parse(args.load)
        abacus.load(value, cell)
    if args.push is not None:
        force, cell = call_parse(args.push)
        abacus.push(abacus.val[cell], force)
    if args.pull is not None:
        force, cell = call_parse(args.pull)
        abacus.pull(abacus.val[cell], force)
    if args.add is not None:
        abacus.add1(decide_base(args.add))
    if args.sub is not None:
        abacus.sub1(decide_base(args.sub))
    if args.sub_from is not None:
        abacus.subfrom1(decide_base(args.sub_from))
    if args.multi is not None:
        abacus.mult1(decide_base(args.multi))
    if args.div is not None:
        abacus.div1(decide_base(args.div))
    if args.ico:
        numi = table_num_listise()
        print(icositetrise(numi))

    abacus.prnt(tee=not Aba.verbose)
    if Aba.verbose:
        print("FIN")

"""TODO: print and input as quad-seximal 
DONE: Input Error handling
base24 input.
Color to cell"""
