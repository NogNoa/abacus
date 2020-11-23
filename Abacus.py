verbose = True


def initorder(obj, mother):
    mother = mother.val
    pl = mother.index(obj)
    return mother, pl


def length24(call):
    log = (0, 24, 576, 13824, 331776, 24 ** 5)
    back = 0
    for n in log:
        if call >= n:
            back = log.index(n)
        else:
            break
    return back + 1


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
        dr = - 1 + (2 * push)  # direction push = +1 pull = -1
        if push == self.up:
            # only work in the right direction, when reaching the other end it returns to the cell
            cell, pl = self.cell, self.pl
            pl_nxt = cell.index(self) - dr
            force = cell[pl_nxt].push_pull(force, push)
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
        self.push_pull(force, push=True)

    def pull(self, force=1):
        self.push_pull(force, push=False)

    def set_clear(self, st: bool):
        for b in self.val[1:-1]:
            b.up = st

    def set(self):
        self.set_clear(st=True)

    def clear(self):
        self.set_clear(st=False)

    def load(self, const):
        if const >= 24**6:
            print(f'Very funny. The input {const} is too big for my brain. '
                  f'I\'m not wasting my time. Try {24 ** 6 - 1} max.')
            const = 0
        self.clear()
        self.push(const)

    def numerise(self):
        back = 0
        for b in self.val[1:-1]:
            if b.up:
                back += 1
        return back


class Abacus:
    def __init__(self):
        self.c00 = Cell('big', 'c00', 'red', )
        self.c06 = Cell('small', 'c06', 'red')
        self.c10 = Cell('big', 'c10', 'yellow')
        self.c16 = Cell('small', 'c16', 'yellow')
        self.c20 = Cell('big', 'c20', 'green')
        self.c26 = Cell('small', 'c26', 'green')
        self.c30 = Cell('big', 'c30', 'blue')
        self.c36 = Cell('small', 'c36', 'blue')
        self.c40 = Cell('big', 'c40', 'indigo')
        self.c46 = Cell('small', 'c46', 'indigo')
        self.c50 = Cell('big', 'c50', 'violet')
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
                        back += '||-\t'
                    else:
                        if not up:
                            back += '---\t' * 3
                        back += '-||\t'
                elif b.up == up:  # type(b) == beed
                    back += '-O-\t'
                else:  # b.up != up:
                    back += '---\t' * 3 + '-O-\t'
                    up = True
            if self.val.index(c) % 2:
                back += c.color + '\n'
        return back

    def prnt(self, table='abacus.csv', tee=False):
        back = self.expose()
        if tee:
            print(back)
        back = back.replace('\t', ',')
        open(table, 'w+').write(back)

    def flow(self, over):
        if over:
            self.overflow = True
        else:
            self.underflow = True

    def clear(self):
        for c in self.val:
            c.clear()

    # note no set, making a macro for this is superfluous.

    def load(self, call, cell_0=0, lngth=1):
        for c in range(1, lngth):
            self.val[cell_0 + c].clear()
        # clears lngth-1 cells, starting from the one after cell_0. cell_0 will already be cleared by load()
        self.val[cell_0].load(call)
        if verbose:
            print(f'Loading {call} at row {int(cell_0 / 2)}', self.expose(), sep='\n')

    def magnitude(self):
        back = 6
        for i in range(6):
            icositetrigit = self.val[-2 * i - 1].numerise() or self.val[-2 * i - 2].numerise()
            if icositetrigit == 0:
                back -= 1
            else:
                break
        if verbose:
            print(f'Mesuring the order magnitude of loaded value as {back}\n')
        return back

    def right(self):
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
        self.c56.clear()
        for c in self.val[:1:-1]:
            nxt = self.val[c.pl - 2]
            while nxt.numerise() != 0:
                nxt.pull()
                c.push()
        if verbose:
            print('Moving down', self.expose(), sep='\n')

    def add1(self, call, cell_0=0):
        self.val[cell_0].push(call)
        if verbose:
            print(f'Adding {call} at row {int(cell_0 / 2)}', self.expose(), sep='\n')

    def sub1(self, call, cell_0=0):
        self.val[cell_0].pull(call)
        if verbose:
            print(f'subtracting {call} at row {int(cell_0 / 2)}', self.expose(), sep='\n')

    def addition(self, augend, *addendi):
        self.overflow = False
        self.clear()
        self.load(augend)
        for a in addendi:
            self.add1(a)
        if self.overflow:
            print("I got overflowed\n")

    def subtraction(self, minuend, *subtrendi):
        self.underflow = False
        self.clear()
        self.load(minuend)
        for s in subtrendi:
            self.sub1(s)
        if self.underflow:
            print("I got undrflowed\n")

    def multiplication(self, multiplier, multiplicand):
        self.clear()
        self.load(multiplicand)
        lngth_cand = self.magnitude()
        self.clear()
        self.load(multiplier)
        lngth = self.magnitude()
        if lngth_cand > 5:
            if lngth > 5:
                print(f'Sorry chemp, both {multiplier} and {multiplicand} are too big. '
                      f'Try to have at least one of them as {24 ** 5 - 1} or smaller\n')
            else:
                if verbose:
                    print('Flipping the factors and going again\n')
                self.multiplication(multiplicand, multiplier)
            return
        for count in range(lngth):
            while not (self.c00.numerise() or self.c06.numerise() == 0):
                self.c00.pull()
                self.add1(multiplicand, cell_0=min(lngth * 2, 10))
            if count < 5:
                self.right()
        if self.overflow:
            print("I got overflowed\n")


if __name__ == "__main__":
    abacus = Abacus()
    abacus.multiplication(24 ** 5, 24 ** 5)
    abacus.prnt(tee=True)


""" max add around 840-850
TODO: cli
replace length24
Done: how to treat the carry and borrow flags
treat the clear issue
trying to make a function that will actually be more localised to the one beed, 
at the price of running more of them, it will also be more ready to add carry.
will probably want to seperate push and pull anyway"""
