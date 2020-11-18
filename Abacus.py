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

    def push_pull(self, push: bool, force: int):
        if force < 1:
            return force
        cell, pl = self.cell, self.pl
        dr = - 1 + (2 * push)  # direction push = +1 pull = -1
        if self.up != cell[pl + dr].up:
            self.up = not self.up
            force -= 1
        force = cell[pl - dr].push_pull(push, force)
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

    def push_pull(self, push, force: int):
        if force < 1:
            return force
        push = bool(push)
        dr = - 1 + (2 * push)  # direction push = +1 pull = -1
        if push == self.up:
            # only work in the right direction, when reaching the other end it returns to the cell
            cell, pl = self.cell, self.pl
            pl_nxt = cell.index(self) - dr
            force = cell[pl_nxt].push_pull(push, force)
        return force


class Cell:
    def __init__(self, size, cid, color):
        self.id = cid
        self.size = (size == 'big')
        self.color = color
        self.bottom = End(False)
        self.abacus = []
        self.pl = 0
        self.didcarry = False
        self.didborrow = False

        self.b1 = Beed(cid + '.b1')
        self.b2 = Beed(cid + '.b2')
        self.b3 = Beed(cid + '.b3')
        self.val = [self.bottom, self.b1, self.b2, self.b3]
        if self.size:
            self.b4 = Beed(cid + '.b4')
            self.b5 = Beed(cid + '.b5')
            self.val.extend([self.b4, self.b5])
        self.top = End(True)
        self.val.append(self.top)
        for b in self.val:
            b.cell, b.pl = initorder(b, self)

    def expose(self):
        return [(i.expose(), i.id) for i in self.val]

    def push_pull(self, push, force):
        force = self.val[push * -1].push_pull(push, force)
        while force > 0:
            """ push_pull by 1 the next cell  \
            clear_set the cell,  \
            and aplly the push_pull to itself again s.t force -= 1"""
            if self.id != 'c56':
                abacus.val[self.pl + 1].push_pull(push, 1)  # cell[-1] is top cell[0] is bottom
            self.set_clear(not push)
            force = self.val[push * -1].push_pull(push, force - 1)

    def push(self, force):
        self.push_pull(True, force)

    def pull(self, force):
        self.push_pull(False, force)

    def set_clear(self, st: bool):
        for b in self.val:
            if type(b) == Beed:
                b.up = st

    def set(self):
        self.set_clear(True)

    def clear(self):
        self.set_clear(False)

    """
    def load(self, const):
        pl = self.pl
        self.st_clear(st=True)
        self.abacus[pl + 1].clear()
        if const > 24:
            self.abacus[pl + 2].clear()
            self.abacus[pl + 3].clear()
        self.push(const)
    """

    def numerise(self):
        back = 0
        for b in self.val:
            if type(b) == Beed and b.up:
                back += 1
        return back


class Abacus:
    def __init__(self):
        self.c00 = Cell('big', 'c00', 'red')
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
        self.c56 = Cell('small', 'c56', 'violet')
        self.val = (self.c00, self.c06, self.c10, self.c16, self.c20, self.c26,
                    self.c30, self.c36, self.c40, self.c46, self.c50, self.c56)
        for c in self.val:
            c.abacus, c.pl = initorder(c, self)

    def prnt(self, table='abacus.csv'):
        table = open(table, 'w+')
        for c in self.val:
            up = False
            for b in c.val:
                if type(b) == End:
                    if not b.up:
                        table.write('||-,')
                    else:
                        if not up:
                            table.write('---,' * 3)
                        table.write('-||,')
                elif b.up == up:  # type(b) == beed
                    table.write('-O-,')
                else:  # b.up != up:
                    table.write('---,' * 3 + '-O-,')
                    up = True
            if self.val.index(c) % 2:
                table.write(c.color + '\n')

    def new_expose(self):
        back = ''
        for c in self.val:
            up = False
            for b in c.val:
                if type(b) == End:
                    if not b.up:
                        back += '||-,'
                    else:
                        if not up:
                            back += '---,' * 3
                        back += '-||,'
                elif b.up == up:  # type(b) == beed
                    back += '-O-,'
                else:  # b.up != up:
                    back += '---,' * 3 + '-O-,'
                    up = True
            if self.val.index(c) % 2:
                back += c.color + '\n'
        back = back.replace(',', '\t')
        print(back)

    def expose(self, table='abacus.csv'):
        self.prnt(table)
        table = open(table, 'r+').read()
        table = table.replace(',', '\t')
        print(table)

    def clear(self):
        for c in self.val:
            c.set_clear(False)

    def load(self, call, row=0):
        if call < 24 ** 2:
            self.val[2 * row].load(call)
        elif call < 2870:
            call = call - 830
            self.load(call, row)
            self.val[2 * row].push(830)
        else:
            horn = call // 24 ** 2
            call = call % 24 ** 2
            self.load(call, row)
            self.load(horn, row + 2)

    def add1(self, call, row=0):
        if call < 830:
            self.val[2 * row].push(call)
        elif call < 2870:
            call = call - 830
            self.add1(call, row)
            self.val[2 * row].push(830)
        else:
            horn = call // 24 ** 2
            call = call % 24 ** 2
            self.add1(call, row)
            self.add1(horn, row + 2)


if __name__ == "__main__":
    abacus = Abacus()
    abacus.c00.push_pull(True, 300)
    # abacus.c00.set_clear(False)
    # abacus.c00.top.push_pull(True, 840)
    # abacus.c00.top.push_pull(True, 849)
    # abacus.load(2869)
    abacus.expose()
    print(abacus.c06.numerise())

""" max add around 840-850
TODO: treat the clear issue
Done:.trying to make a function that will actually be more localised to the one beed, 
at the price of running more of them, it will also be more ready to add carry.
will probably want to seperate push and pull anyway"""
