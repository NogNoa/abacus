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
        self.abacus = []
        self.pl = 0
        self.didcarry = False
        self.didborrow = False

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
        self.push_pull(push=True, force=force)

    def pull(self, force):
        self.push_pull(push=False, force=force)

    def set_clear(self, st: bool):
        for b in self.val[1:-1]:
            b.up = st

    def set(self):
        self.set_clear(st=True)

    def clear(self):
        self.set_clear(st=False)

    def load(self, const):
        self.set_clear(st=False)
        # self.abacus[pl + 1].clear()
        self.push(const)

    def numerise(self):
        back = 0
        for b in self.val[1:-1]:
            if b.up:
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

    def clear(self):
        for c in self.val:
            c.set_clear(False)

    def load(self, call, cell_0=0, lngth=1):
        for c in range(1, lngth):
            self.val[cell_0 + c].clear()
        # clears lngth-1 cells, starting from the one after cell_0. cell_0 will already be cleared by load()
        self.val[cell_0].load(call)

    def add1(self, call, cell_0=0):
        self.val[cell_0].push(call)

    def sub1(self,call, cell_0=0):
        self.val[cell_0].pull(call)

    def addition(self, augend, *addendi):
        self.load(augend)
        for a in addendi:
            self.add1(a)

    def subtraction(self, minuend, *subtrendi):
        self.load(minuend)
        for s in subtrendi:
            self.sub1(s)
            

if __name__ == "__main__":
    abacus = Abacus()
    #abacus.c00.push(3000)
    """
    # abacus.c00.set_clear(False)
    # abacus.c00.top.push_pull(push=True, 840)
    # abacus.c00.top.push_pull(push=True, 849)
    # abacus.load(2869)
    # abacus.expose()
    for c in abacus.val:
        print(c.id, c.numerise())
    abacus.load(3, 1, lngth=1)
    """
    abacus.subtraction(3000, 300, 24)
    abacus.prnt(tee=True)


""" max add around 840-850
TODO: how to treat the carry and borrow flags
Done: treat the clear issue
trying to make a function that will actually be more localised to the one beed, 
at the price of running more of them, it will also be more ready to add carry.
will probably want to seperate push and pull anyway"""
