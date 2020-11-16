def initorder(obj, mother):
    mother = mother.val
    pl = mother.index(obj)
    return mother, pl


class beed:
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

    def old_push(self, force):
        """pusshes up as much beeds as the given force"""
        cell, pl = self.cell, self.pl
        force = min(len(cell) - 2, force)  # putting a ceiling on force avoids index error
        if cell[pl + force].up:
            for b in cell[pl:pl + force]:
                b.up = True
        else:
            cell[pl + 1].old_push(force)
        """notable sideefect: inputting negative force works. 
        for big cell -1=0 -2=5 -3=4 and so forth until -8.
         -9 is out of range.
        for small cells it's goes down to -6 and fails at -7
        """

    def old_pull(self, force):
        cell, pl = self.cell, self.pl
        force = min(len(cell) - 2, force)  # putting a ceiling on force avoids index error
        if not cell[pl - force].up:
            for b in cell[pl - force + 1:pl + 1]:
                b.up = False
        else:
            cell[pl - 1].old_pull(force)

    def push_pull(self, push: bool, force: int):
        if force < 1:
            return
        cell, pl = self.cell, self.pl
        dr = - 1 + (2 * push)  # direction
        if self.up != cell[pl + dr]:
            self.up = not self.up
            force -= 1
        cell[pl - dr].push_pull(push, force)


class end:
    def __init__(self, up, mother):
        self.up = up
        self.id = 'end'
        self.cell = []
        self.pl = 0
        self.mother = mother

    def old_push(self, force):
        if self.up:
            return
        else:
            cell, pl = self.cell, self.pl
            pl = cell.index(self)
            cell[pl + 1].old_push(force)

    def old_pull(self, force):
        if self.up:
            cell, pl = self.cell, self.pl
            pl = cell.index(self)
            cell[pl - 1].old_pull(force)
        else:
            return

    def expose(self):
        if self.up:
            return 'Top'
        else:
            return 'Bottom'

    def push_pull(self, push, force: int):
        if force < 1:
            return
        push = bool(push)
        dr = - 1 + (2 * push)  # direction
        if push == self.up:
            cell, pl = self.cell, self.pl
            pl_nxt = cell.index(self) - dr
            cell[pl_nxt].push_pull(push, force)
        else:
            nxt_cell = abacus.val[self.mother.pl + dr].val
            nxt_cell[push * -1].push_pull(push, 1)
        # just seperate them damnit



class cell:
    def __init__(self, size, cid, color):
        self.id = cid
        self.size = (size == 'big')
        self.color = color
        self.bottom = end(False, self)
        self.abacus = []
        self.pl = 0
        self.b1 = beed(cid + '.b1')
        self.b2 = beed(cid + '.b2')
        self.b3 = beed(cid + '.b3')
        self.val = [self.bottom, self.b1, self.b2, self.b3]
        if self.size:
            self.b4 = beed(cid + '.b4')
            self.b5 = beed(cid + '.b5')
            self.val.extend([self.b4, self.b5])
        self.top = end(True, self)
        self.val.append(self.top)
        for b in self.val:
            b.cell, b.pl = initorder(b, self)

    def expose(self):
        return [(i.expose(), i.id) for i in self.val]


class abacus:
    def __init__(self):
        self.c00 = cell('big', 'c00', 'red')
        self.c06 = cell('small', 'c06', 'red')
        self.c10 = cell('big', 'c10', 'yellow')
        self.c16 = cell('small', 'c16', 'yellow')
        self.c20 = cell('big', 'c20', 'green')
        self.c26 = cell('small', 'c26', 'green')
        self.c30 = cell('big', 'c30', 'blue')
        self.c36 = cell('small', 'c36', 'blue')
        self.c40 = cell('big', 'c40', 'indigo')
        self.c46 = cell('small', 'c46', 'indigo')
        self.c50 = cell('big', 'c50', 'violet')
        self.c56 = cell('small', 'c56', 'violet')
        self.val = (self.c00, self.c06, self.c10, self.c16, self.c20, self.c26,
                    self.c30, self.c36, self.c40, self.c46, self.c50, self.c56)
        for c in self.val:
            c.abacus, c.pl = initorder(c, self)

    def prnt(self, table='abacus.csv'):
        table = open(table, 'w+')
        for c in self.val:
            up = False
            for b in c.val:
                if type(b) == end:
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


abacus = abacus()
abacus.val[0].bottom.old_push(3)
abacus.c00.top.push_pull(False, 1)
print(abacus.c00.expose())
abacus.expose()

"""TODO:.trying to make a function that will actually be more localised to the one beed, 
at the price of running more of them, it will also be more ready to add carry.
will probably want to seperate push and pull anyway"""
