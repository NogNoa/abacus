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

if __name__ == "__main__":
    file = 'abacus.csv'
    abacus = Aba.Abacus()
    try:
        abacus.num_read(table_num_listise(file))
    except FileNotFoundError:
        abacus.clear()
    parser = argparse.ArgumentParser(description=Aba.help_dscrpt)
    parser.add_argument('-v', '--verbose', help="Make me announce more stuff", action="store_true")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument('--up', help=abacus.right.__doc__, action="count")
    actions.add_argument('--down', help=abacus.left.__doc__, action="count")
    actions.add_argument('--clear', help=Aba.Cell.clear.__doc__, type=int)
    actions.add_argument('--set', help=Aba.Cell.set.__doc__, type=int)
    actions.add_argument('--add', help=abacus.add1.__doc__, type=int)
    actions.add_argument('--sub', help=abacus.sub1.__doc__, type=int)
    actions.add_argument('--multi', help=abacus.mult1.__doc__, type=int)
    actions.add_argument('--load', help=Aba.Cell.load.__doc__)
    actions.add_argument('--push', help=Aba.Cell.push.__doc__)
    actions.add_argument('--pull', help=Aba.Cell.pull.__doc__)
    actions.add_argument('--clear_full', help=abacus.clear.__doc__, action="store_true")
    actions.add_argument('--load_full', help=abacus.load.__doc__, type=int)


    args = parser.parse_args()
    if args.verbose:
        Aba.verbose = True
    if args.clear_full:
        abacus.clear()
    if args.load_full is not None:
        abacus.load(args.load_full)
    if args.up:
        for i in range(args.up):
            abacus.right()
    if args.down:
        for i in range(args.down):
            abacus.left()
    if args.clear is not None:
        abacus.val[args.clear].clear()
    if args.set is not None:
        abacus.val[args.set].set()

    if args.load is not None:
        call = args.load
        if len(call) == 2:
            cell = int(call[0])
            value = int(call[1])
            abacus.val[cell].load(value)
        else:
            print('please enter two arguments, first the cell number, second the value to load'
                  '\n Format: "Cell,Value" without a space.')
    if args.push is not None:
        call = args.push
        if len(call) == 2:
            cell = int(call[0])
            force = int(call[1])
            abacus.val[cell].push(force)
        else:
            print('please enter two arguments, first the cell number, second the value to push'
                  '\n Format: "Cell,Value" without a space.')
    if args.pull is not None:
        call = args.pull
        if len(call) == 2:
            cell = int(call[0])
            force = int(call[1])
            abacus.val[cell].pull(force)
        else:
            print('please enter two arguments, first the cell number, second the value to pull.'
                  '\n Format: "Cell,Value" without a space.')

    if args.add is not None:
        abacus.add1(args.add)
    if args.sub is not None:
        abacus.sub1(args.sub)
    if args.multi is not None:
        abacus.mult1(args.multi)

    abacus.prnt(tee=not Aba.verbose)
    if Aba.verbose:
        print("FIN")
    """
    num = table_num_listise()
    print(num)   
    print(decimate(num))
    """

"""Todo:base24 input."""