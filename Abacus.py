help_dscrpt = \
    """
An interactive quad-seximal abacus for fun.
The Abacus have 12 cells in 6 rows numbered 0 to 5.
Each row has a lower cell with 5 beeds and a high cell with 3 beeds.
The full cell is a distinct state, only when you add one to it does the next cell change 
    and the first one empties.
This make the abacus base 24 by row.
"""

verbose = False


def initorder(obj, mother):
    mother = mother.val
    pl = mother.index(obj)
    return mother, pl


class Beed:
    def __init__(self, bid):
        self.up = False
        self.id = bid
        self.cell = []
        self.pl = 0

    def expose(self):
        if self.up:
            return 'Up'
        else:
            return 'Down'

    def push_pull(self, force: int, push: bool):
        if force < 1:
            return force
        cell, pl = self.cell, self.pl
        dr = - 1 + (2 * push)  # direction push = +1 pull = -1
        if self.up != cell[pl + dr].up:
            self.up = not self.up
            force -= 1
        force = cell[pl - dr].push_pull(force, push)
        return force


class End:
    def __init__(self, up):
        self.up = up
        self.id = 'end'
        self.cell = []
        self.pl = 0

    def expose(self):
        if self.up:
            return 'Top'
        else:
            return 'Bottom'

    def push_pull(self, force: int, push: bool):
        if force < 1:
            return force
        if push == self.up:
            # only does work in the right direction, when reaching the other end it returns to the cell
            cell, pl = self.cell, self.pl
            dr = - 1 + (2 * push)  # direction push = +1 pull = -1
            force = cell[pl - dr].push_pull(force, push)
        return force


class Cell:
    def __init__(self, size, cid, color, mother=None):
        self.id = cid
        self.size = (size == 'big')
        self.color = color
        self.abacus = []
        self.pl = 0
        self.mother = mother

        self.bottom = End(up=False)
        self.b1 = Beed(cid + '.b1')
        self.b2 = Beed(cid + '.b2')
        self.b3 = Beed(cid + '.b3')
        self.val = [self.bottom, self.b1, self.b2, self.b3]
        if self.size:
            self.b4 = Beed(cid + '.b4')
            self.b5 = Beed(cid + '.b5')
            self.val.extend([self.b4, self.b5])
        self.top = End(up=True)
        self.val.append(self.top)
        for b in self.val:
            b.cell, b.pl = initorder(b, self)

    def expose(self):
        return [(i.expose(), i.id) for i in self.val]

    def push_pull(self, force, push):
        if force >= 24 ** 6:
            print(f'\nVery funny. The input {force} is too big for my brain. '
                  f'I\'m not wasting my time. Try {24 ** 6 - 1} max.\n')
            self.mother.flow(over=push)
            force = 0
        force = self.val[push * -1].push_pull(force, push)
        while force > 0:
            """ push_pull by 1 the next cell  \
            clear_set the cell,  \
            and aplly the push_pull to itself again s.t force -= 1"""
            if self.id != 'c56':
                abacus.val[self.pl + 1].push_pull(1, push)  # cell[-1] is top cell[0] is bottom
            else:
                self.mother.flow(over=push)
            self.set_clear(st=not push)
            force = self.val[push * -1].push_pull(force - 1, push)

    def push(self, force=1):
        """Move beeds to the Right of the cell"""
        self.push_pull(force, push=True)

    def pull(self, force=1):
        """Return beeds to the Left of the cell"""
        self.push_pull(force, push=False)

    def set_clear(self, st: bool):
        for b in self.val[1:-1]:
            b.up = st

    def set(self):
        """Move all beeds to the Right of the cell."""
        self.set_clear(st=True)

    def clear(self):
        """Return all beeds to the Left of the cell, reseting it to Zero."""
        self.set_clear(st=False)

    def load(self, const):
        """Set the cell to a speicific number."""
        self.clear()
        self.push(const)

    def numerise(self):
        back = 0
        for b in self.val[1:-1]:
            if b.up:
                back += 1
        return back

    def not_zero(self):
        return self.val[0].up


class Abacus:
    def __init__(self):
        self.c00 = Cell('big', 'c00', 'red', self)
        self.c06 = Cell('small', 'c06', 'red', self)
        self.c10 = Cell('big', 'c10', 'yellow', self)
        self.c16 = Cell('small', 'c16', 'yellow', self)
        self.c20 = Cell('big', 'c20', 'green', self)
        self.c26 = Cell('small', 'c26', 'green', self)
        self.c30 = Cell('big', 'c30', 'blue', self)
        self.c36 = Cell('small', 'c36', 'blue', self)
        self.c40 = Cell('big', 'c40', 'indigo', self)
        self.c46 = Cell('small', 'c46', 'indigo', self)
        self.c50 = Cell('big', 'c50', 'violet', self)
        self.c56 = Cell('small', 'c56', 'violet', self)
        self.val = (self.c00, self.c06, self.c10, self.c16, self.c20, self.c26,
                    self.c30, self.c36, self.c40, self.c46, self.c50, self.c56)
        for c in self.val:
            c.abacus, c.pl = initorder(c, self)
        self.overflow = False
        self.underflow = False

    def expose(self):
        back = ''
        for c in self.val:
            up = False
            for b in c.val:
                if type(b) == End:
                    if not b.up:
                        back += '||- '
                    else:
                        if not up:
                            back += '--- ' * 3
                        back += '-|| '
                elif b.up == up:  # type(b) == beed
                    back += '-O- '
                else:  # b.up != up:
                    back += '--- ' * 3 + '-O- '
                    up = True
            if self.val.index(c) % 2:
                back += c.color + '\n'
        return back

    def prnt(self, table='abacus.csv', tee=False):
        back = self.expose()
        if tee:
            print(back)
        back = back.replace(' ', ',')
        open(table, 'w+').write(back)

    def num_read(self, call: list) -> None:
        for pl, num in enumerate(call):
            self.val[pl].load(num)

    def flow(self, over):
        if over:
            self.overflow = True
        else:
            self.underflow = True

    def clear(self):
        """Clear every Cell of the abacus"""
        self.overflow = False
        self.underflow = False
        for c in self.val:
            c.clear()

    # note no set, making a macro for this is superfluous.

    def load(self, call, cell_0=0):
        """Set the abacus to a specific number"""
        if verbose:
            print(f'Loading {call} at row {int(cell_0 / 2)}')
        self.clear()
        # clears lngth-1 cells, starting from the one after cell_0. cell_0 will already be cleared by load()
        self.val[cell_0].load(call)
        if verbose:
            print(self.expose())

    def magnitude(self):
        if self.overflow:
            return 7
        if self.underflow:
            return -1
        back = 6
        for i in range(6):
            icositetrigit = self.val[-2 * i - 1].not_zero() or self.val[-2 * i - 2].not_zero()  # base 24 digit
            if not icositetrigit:
                back -= 1
            else:
                break
        if verbose:
            print(f'Mesuring the base-24 order of magnitude of loaded value as {back}\n')
        return back

    def right(self):
        """Moves all cells Up"""
        self.c00.clear()
        # c56 is the one that's actually end up cleared, as the last nxt
        for c in self.val[:-2]:
            nxt = self.val[c.pl + 2]
            while nxt.numerise() != 0:
                nxt.pull()
                c.push()
        if verbose:
            print('Moving up', self.expose(), sep='\n')

    def left(self):
        """Moves all cells Down"""
        self.c56.clear()
        for c in self.val[:1:-1]:
            nxt = self.val[c.pl - 2]
            while nxt.numerise() != 0:
                nxt.pull()
                c.push()
        if verbose:
            print('Moving down', self.expose(), sep='\n')

    def add1(self, call, cell_0=0):
        if verbose:
            print(f'Adding {call} at row {int(cell_0 / 2)}')
        self.val[cell_0].push(call)
        if verbose:
            print(self.expose())

    def sub1(self, call, cell_0=0):
        if verbose:
            print(f'subtracting {call} at row {int(cell_0 / 2)}')
        self.val[cell_0].pull(call)
        if verbose:
            print(self.expose())

    def addition(self, augend, *addendi):
        self.overflow = False
        if not augend is None:  # For useing former answer
            self.load(augend)
        for a in addendi:
            self.add1(a)
        if self.overflow:
            print("I got overflowed\n")

    def subtraction(self, minuend, *subtrendi):
        self.underflow = False
        if not minuend is None:  # For useing former answer
            self.load(minuend)
        for s in subtrendi:
            self.sub1(s)
        if self.underflow:
            print("I got undrflowed\n")

    def multiplication(self, multiplier, multiplicand):
        self.overflow = False
        # Mesuring the factors
        self.load(multiplicand)
        lngth_cand = self.magnitude()
        self.load(multiplier)
        lngth = self.magnitude()

        # High edge cases
        if lngth_cand + lngth > 7:
            print(f'Sorry chemp, both {multiplier} and {multiplicand} are too big. '
                  f'Try to have their order of magnitude sum as 7 or less.')
            self.clear()
            return

        # The main operation
        for count in range(lngth):
            while self.c00.numerise() or self.c06.numerise():
                self.c00.pull()
                self.add1(multiplicand, cell_0=min(lngth * 2, (6 - lngth_cand) * 2, 10))
            if count < min((6 - lngth_cand), 5):
                self.right()
        if self.overflow:
            print("I got overflowed\n")

    def multi_multiplication(self, multplicand, *multiplieri):
        self.multiplication(multiplieri[0], multplicand)
        for m in multiplieri[1:]:
            self.mult1(m)

    def mult1(self, multiplicand):
        self.overflow = False
        lngth = self.magnitude()
        try:
            self.val[lngth * 2].push(multiplicand)
        except IndexError:
            self.flow(over=True)
        if self.overflow or self.c50.not_zero() or self.c56.not_zero():
            print(f'Sorry chemp, both previous answer and {multiplicand} were too big. '
                  f'Try to have their order of magnitude sum as 7 or less.')
            return
        self.val[lngth * 2].pull(multiplicand)
        for count in range(lngth):
            while self.c00.numerise() or self.c06.numerise():
                self.c00.pull()
                self.add1(multiplicand, cell_0=lngth * 2)
            self.right()
        if self.overflow:
            print("I got overflowed\n")


if __name__ == "__main__":
    verbose = True
    abacus = Abacus()
    # abacus.multiplication(24 ** 2, 24 ** 4 - 1)
    # abacus.num_read([4, 2, 0, 0, 5, 3, 5, 3, 5, 3, 5, 1]
    abacus.multi_multiplication(24, 7, 8)
    abacus.c00.load(4)
    abacus.prnt(tee=True)

"""
TODO: cli
more rebust solution for length_lier+length_cand = 5
Done: replace length24
how to treat the carry and borrow flags
treat the clear issue
trying to make a function that will actually be more localised to the one beed, 
at the price of running more of them, it will also be more ready to add carry.
will probably want to seperate push and pull anyway"""

"""
row to write to = lngth + length_cand - 2 (starting at 0)
too big row = 5
too big lngth = 7 - length_cand
for 0 5
for 1 4
for 2 3
"""
