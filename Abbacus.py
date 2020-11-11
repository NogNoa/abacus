class beed:
    def __init__(self, bid, cell):
        self.id = bid
        self.up = False
        self.cell = cell

    def expose(self):
        if self.up:
            return 'Up'
        else:
            return 'Down'

    def initpushpull(self, force):
        dgt = self.cell.val
        force = min(len(dgt) - 2, force)  # putting a ceiling on force avoids index error
        pl = dgt.index(self)
        return dgt, force, pl

    def push(self, force):
        """pusshes up as much beeds as the given force"""
        dgt, force, pl = self.initpushpull(force)
        if dgt[pl + force].up:
            for b in dgt[pl:pl + force]:
                b.up = True
        else:
            dgt[pl + 1].push(force)
        """notable sideefect: inputting negative force works. 
        for big cell -1=0 -2=5 -3=4 and so forth until -8.
         -9 is out of range.
        for small cells it's goes down to -6 and fails at -7
        """

    def pull(self, force):
        dgt, force, pl = self.initpushpull(force)
        if not dgt[pl - force].up:
            for b in dgt[pl - force + 1:pl + 1]:
                b.up = False
        else:
            dgt[pl - 1].pull(force)

    def draft_pushpull(self, push: bool, force: int):
        dgt = self.cell.val
        pl = dgt.index(self)
        nxt = dgt[pl - 1 + (2 * push)]
        if push == self.up:




class end:
    def __init__(self, up, cell):
        self.up = up
        self.id = 'end'
        self.cell = cell

    def push(self, force):
        if self.up:
            return
        else:
            dgt = self.cell.val
            pl = dgt.index(self)
            dgt[pl + 1].push(force)

    def pull(self, force):
        if self.up:
            dgt = self.cell.val
            pl = dgt.index(self)
            dgt[pl - 1].pull(force)
        else:
            return

    def expose(self):
        if self.up:
            return 'Top'
        else:
            return 'Bottom'

    def draft_pushpull(self, push: bool, force: int):
        if push == self.up:
            print('carry')
        else:
            dgt = self.cell.val
            pl_nxt = dgt.index(self) - 1 + (2 * push)
            dgt[pl_nxt].draftpushpull(push, force)



class cell:
    def __init__(self, size, cid):
        self.id = cid
        self.size = (size == 'big')
        self.bottom = end(0, self)
        self.b1 = beed(cid + '.b1', self)
        self.b2 = beed(cid + '.b2', self)
        self.b3 = beed(cid + '.b3', self)
        self.val = [self.bottom, self.b1, self.b2, self.b3]
        if self.size:
            self.b4 = beed(cid + '.b4', self)
            self.b5 = beed(cid + '.b5', self)
            self.val.extend([self.b4, self.b5])
        self.top = end(1, self)
        self.val.append(self.top)

    def expose(self):
        return [(i.expose(), i.id) for i in self.val]


c00 = cell('big', 'c00')
c06 = cell('small', 'c06')
c10 = cell('big', 'c10')
c16 = cell('small', 'c16')
c20 = cell('big', 'c20')
c26 = cell('small', 'c26')
c30 = cell('big', 'c30')
c36 = cell('small', 'c36')
c40 = cell('big', 'c40')
c46 = cell('small', 'c46')
c50 = cell('big', 'c50')
c56 = cell('small', 'c56')

c06.bottom.push(3)
c06.b3.pull(1)
print(c06.expose())

"""TODO:.trying to make a function that will actually be more localised to the one beed, 
at the price of running more of them, it will also be more ready to add carry.
will probably want to seperate push and pull anyway"""