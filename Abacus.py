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
            return
        cell, pl = self.cell, self.pl
        dr = - 1 + (2 * push)  # direction push = +1 pull = -1
        if self.up != cell[pl + dr].up:
            self.up = not self.up
            force -= 1
        cell[pl - dr].push_pull(push, force)


class End:
    def __init__(self, up, mother):
        self.up = up
        self.id = 'end'
        self.cell = []
        self.pl = 0
        self.mother = mother

    def expose(self):
        if self.up:
            return 'Top'
        else:
            return 'Bottom'

    def push_pull(self, push, force: int):
        if force < 1:
            return
        push = bool(push)
        dr = - 1 + (2 * push)  # direction push = +1 pull = -1
        if push == self.up:
            cell, pl = self.cell, self.pl
            pl_nxt = cell.index(self) - dr
            cell[pl_nxt].push_pull(push, force)
        else:
            if self.mother.id != 'c56':
                nxt_cell = abacus.val[self.mother.pl + 1].val
                nxt_cell[push * -1].push_pull(push, 1)  # cell[-1] is top cell[0] is bottom
            for b in self.cell:
                if type(b) == Beed:
                    b.up = not push
            self.cell[push * -1].push_pull(push, force - 1)


class Cell:
    def __init__(self, size, cid, color):
        self.id = cid
        self.size = (size == 'big')
        self.color = color
        self.bottom = End(False, self)
        self.abacus = []
        self.pl = 0
        self.b1 = Beed(cid + '.b1')
        self.b2 = Beed(cid + '.b2')
        self.b3 = Beed(cid + '.b3')
        self.val = [self.bottom, self.b1, self.b2, self.b3]
        if self.size:
            self.b4 = Beed(cid + '.b4')
            self.b5 = Beed(cid + '.b5')
            self.val.extend([self.b4, self.b5])
        self.top = End(True, self)
        self.val.append(self.top)
        for b in self.val:
            b.cell, b.pl = initorder(b, self)

    def expose(self):
        return [(i.expose(), i.id) for i in self.val]

    def push(self, force):
        self.top.push_pull(True, force)

    def pull(self, force):
        self.bottom.push_pull(False, force)

    def clear(self):
        for b in self.val:
            if type(b) == Beed:
                b.up = False

    def load(self, const):
        self.clear()
        self.push(const)

    def numerise(self):
        back = 0
        for b in self.val:
            if type(b) == Beed:
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

    def expose(self, table='abacus.csv'):
        self.prnt(table)
        table = open(table, 'r+').read()
        table = table.replace(',', '\t')
        print(table)

    def clear(self):
        for c in self.val:
            c.clear()

    def load(self, const, row=0):
        if const < 24 ** 2:
            self.val[2 * row].load(const)
        else:
            horn = const // 24 ** 2
            const = const % 24 ** 2
            self.load(const, row)
            self.load(horn, row + 2)






abacus = Abacus()
#abacus.c00.top.push_pull(True, 853)
#abacus.c00.top.push_pull(True, 840)
#abacus.c00.top.push_pull(True, 849)
abacus.load(3000)
print(abacus.c00.expose())
print(abacus.c56.expose())
abacus.expose()

""" max add around 840-850
Done:.trying to make a function that will actually be more localised to the one beed, 
at the price of running more of them, it will also be more ready to add carry.
will probably want to seperate push and pull anyway"""
