help_dscrpt = \
    """
An interactive quad-seximal abacus for fun. 
The Abacus have 12 cells in 6 rods. 
Each rod has a lower cell with 5 beeds and a high cell with 3 beeds. 
When the cell is full this is a distinct state, only when you add one to it does the next cell change 
    and the first one empties. 
This make the abacus base 24 by rod. 
Enter values as base 24 [0123456789abcdefghijklmn]. 
If you want to use base 10, that's still an option! 
Enter rod by color ['Red', 'Yellow', 'Green', 'Blue', 'Indigo', "Violet"]. 
If both inputs are required always enter value before rod. 
    """

verbose = False


def drc(x): return - 1 + (2 * x)  # True : +1; False : -1


def colorise(rod: int):
    return abacus.val[rod].color


def exchange(donor, acceptor):
    while donor.not_zero():
        donor.pull()
        acceptor.push()


def consume(hybris, nemesis):
    while hybris.not_zero():
        hybris.pull()
        nemesis.pull()


class Bead:
    def __init__(self, pl, cid):
        self.up = False
        self.pl = pl
        self.id = cid + '.b' + str(pl)
        self.cell = []

    def __str__(self):
        if self.up:
            return 'Up'
        else:
            return 'Down'

    def __repr__(self):
        return self.id

    def __int__(self):
        return int(self.up)

    def push_pull(self, force: int, push: bool):
        if force < 1:
            return force
        cell, pl = self.cell, self.pl
        dr = drc(push)
        if self.up != cell[pl + dr].up:
            self.up = not self.up
            force -= 1
        force = cell[pl - dr].push_pull(force, push)
        return force


class End:
    def __init__(self, up, cid):
        self.up = up
        self.id = cid + ".e" + str(up * 6)  # .e0 or .e6

    def __str__(self):
        if self.up:
            return 'Top'
        else:
            return 'Bottom'

    def __repr__(self):
        return self.id

    def __int__(self):
        return 0

    def push_pull(self, force: int, push: bool):
        if push == self.up:
            print('Error! While moving beeds on a cell I got to the wrong end.')
            raise IndexError
        return force


class Cell:
    def __init__(self, deck, pl, rid):
        self.id = rid + '.c' + str(pl * 6)  # .c0 or .c6
        self.size = (deck == 'earth')
        self.abacus = []
        self.pl = pl
        self.deck = deck

        self.bottom = End(up=False, cid=self.id)  # self.bottom.pl = 0
        self.b1 = Bead(1, self.id)
        self.b2 = Bead(2, self.id)
        self.b3 = Bead(3, self.id)
        self.val = [self.bottom, self.b1, self.b2, self.b3]
        if self.size:
            self.b4 = Bead(4, self.id)
            self.b5 = Bead(5, self.id)
            self.val.extend((self.b4, self.b5))
        self.top = End(up=True, cid=self.id)  # self.top.pl = 6
        self.val.append(self.top)
        self.e0, self.e6 = self.bottom, self.top
        for b in self.val:
            b.cell = self.val

    def expose(self):
        back = ''
        up = False
        for b in self.val:
            if type(b) == End:
                if not b.up:
                    back += '||- '
                else:
                    if not up:
                        back += '--- '
                        back += '--- ' * 2 * self.size
                    back += '-|| '
            elif b.up == up:  # type(b) == bead
                back += '-O- '
            else:  # b.up != up:
                back += '--- ' + '--- ' * 2 * self.size + '-O- '
                up = True
        return back

    def __str__(self):
        return self.id[3] + '.' + self.deck

    def __repr__(self):
        return str([(str(b), repr(b)) for b in self.val])

    def __int__(self):
        return sum(int(b) for b in self.val)

    def push_pull(self, force, push):
        force = self.val[push * -1 - drc(push)].push_pull(force, push)
        # We pass the operation to bottom of the cell if pull (0 * -1 --1 = 1, first in cell) or to top if push
        # (1 * -1 - 1 = -2, last in cell). For each bead moved force will go down by 1, and the new value
        # will be returned here.
        return force

    def push(self, force=1):
        """Move beeds in a given cell to the Right"""
        self.push_pull(force, push=True)

    def pull(self, force=1):
        """Return beeds in a given cell to the Left"""
        self.push_pull(force, push=False)

    def set_clear(self, st: bool):
        for b in self.val[1:-1]:
            b.up = st  # true->set false->clear

    def set(self):
        """Move all beeds in a given cell to the Right"""
        self.set_clear(st=True)

    def clear(self):
        """Return all beeds in a given cell to the Left, reseting it to Zero."""
        self.set_clear(st=False)

    def load(self, const):
        """Set a given cell to a speicific number."""
        self.clear()
        self.push(const)

    def numerise(self):
        back = 0
        for b in self.val[1:-1]:
            if b.up:
                back += 1
        return back

    def not_zero(self):
        return self.val[-2].up

    def not_full(self):
        return not self.val[1].up

    def not_zero_full(self, push: bool):
        if push:
            return self.not_full()
        else:
            return self.not_zero()


class Rod:
    def __init__(self, pl, color):
        self.pl = pl
        self.id = 'r' + str(pl)
        self.color = color
        self.abacus = []

        self.earth = Cell('earth', 0, self.id)  # lower cell
        self.sky = Cell('sky', 1, self.id)  # upper cell
        self.val = (self.earth, self.sky)
        self.c0, self.c6 = self.earth, self.sky

    def __str__(self):
        return self.id

    def __repr__(self):
        return str([(int(c), str(c)) for c in self.val])

    def __int__(self):
        return int(self.earth) + int(self.sky) * 6

    def quad_sex(self):
        """Has nothing to do with foursomes"""
        return str(int(self.sky)) + str(int(self.earth))

    def expose(self):
        back = self.earth.expose() + self.sky.expose()
        back += self.color + '\n'
        return back

    def set_clear(self, st=False):
        self.earth.set_clear(st)
        self.sky.set_clear(st)

    def push_pull(self, force: int, push: bool):
        force = self.earth.push_pull(force, push)
        if force:
            sky_done = self.sky.push_pull(1, push)
            self.earth.set_clear(st=not push)
            if sky_done:
                self.sky.set_clear(st=not push)
                # we are returning the force as is, the rest of carry/borrow
                # as well as subtracting 1 from force is handled by abacus.
            else:
                force = self.push_pull(force - 1, push)
        return force

    def push_pull2(self, cell: Cell, force: int, push: bool):
        sky_done = False
        while (not sky_done) and force:
            if push and cell.not_full():
                print('Error! I tried to carry while cell is not full')
            elif (not push) and cell.not_zero():
                print('Error! I tried to borrow while cell is not empty')
            # If we got here it means the force was bigger than the number of beads that were down.
            force = cell.push_pull(force, push)
            if cell.size:  # earth->True sky->False
                self.push_pull2(self.sky, 1, push)
            else:
                sky_done = True
            cell.set_clear(st=not push)
            force -= 1
        return force


class Abacus:
    def __init__(self):
        self.r0 = Rod(0, 'Red')
        self.r1 = Rod(1, 'Yellow')
        self.r2 = Rod(2, 'Green')
        self.r3 = Rod(3, 'Blue')
        self.r4 = Rod(4, 'Indigo')
        self.r5 = Rod(5, 'Violet')
        self.val = (self.r0, self.r1, self.r2, self.r3, self.r4, self.r5,)
        self.earth = [r.earth for r in self.val]
        self.sky = [r.sky for r in self.val]
        self.overflow = False
        self.underflow = False
        for c in self.val:
            c.abacus = self.val

    def __repr__(self):
        return str([(r.quad_sex(), str(r)) for r in self.val])

    def __int__(self):
        return sum(int(r) * 24 ** r.pl for r in self.val)

    def quad_sex(self):
        return ':'.join(r.quad_sex() for r in self.val)

    def expose(self):
        back = ''
        for r in self.val:
            back += r.expose()
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

    def chk_flow(self, over):
        if over:
            flow = self.overflow
            word = 'overflowed'
        else:
            flow = self.underflow
            word = 'underflowed'
        if flow:
            print(f"I got {word}\n")

    def push_pull(self, rod: Rod, force: int, push: bool):
        if force >= 24 ** 6:
            print(f'\nVery funny. The input {force} is too big for my brain. '
                  f'I\'m not wasting my time. Try {24 ** 6 - 1} max.\n')
            self.flow(over=push)  # push -> overflow; pull -> underflow
            force = 0
            # if the number is higher than what the abacus could hold in the first place,
            # we set the respective flow flag, and empty the force so the operation will finish
            # wherever control is returned to.
        force = rod.push_pull(force, push)
        while force:
            """
            if push and cell.not_full():
                print('Error! I tried to carry while cell is not full')
            elif (not push) and cell.not_zero():
                print('Error! I tried to borrow while cell is not empty')
            # If we got here it means the force was bigger than the number of beads that were down.
            """
            if rod.id != 'r5':
                self.push_pull(self.val[rod.pl + 1], 1, push)
                # For most cells we pass a carry of 1 to the next cell
            else:
                self.flow(over=push)
                # But if it is the last cell we have to flag the corresponding flow flag instead.
            rod.set_clear(st=not push)  # push-> set, pull-> clear
            force = rod.push_pull(force - 1, push)
            # Then we set or clear the cell and pass a push or pull command to the ends as before.
            # We subtract 1 force to pay for the set/clear. We continue the loop until force is zero.

    def push(self, rod: Rod, force=1):
        """Move beeds in a given cell to the Right"""
        self.push_pull(rod, force, push=True, )

    def pull(self, rod: Rod, force=1):
        """Return beeds in a given cell to the Left"""
        self.push_pull(rod, force, push=False)

    def clear(self, st=False, start=0, verbose=verbose, fromhigh=False):
        """Clear every Cell of the abacus"""
        if fromhigh:
            #  To start from the upper deck of a rod
            self.val[start].sky.set_clear(st)
            start += 1
        for r in self.val[start:]:
            r.set_clear(st)
        if verbose:
            if st:
                print(f'Setting all from the {colorise(start)} rod')
            else:
                print(f'Clearing all from the {colorise(start)} rod')
            print(self.expose())

    # note, making a macro for set is superfluous. But it's implemented by Truing st.

    def load(self, call, start=0):
        """Set the abacus to a specific number"""
        self.overflow = False
        self.clear(verbose=False, start=start)
        # clears length-1 cells, starting from the one after cell_0. cell_0 will already be cleared by load()
        self.push(self.val[start], call)
        self.chk_flow(over=True)
        if verbose:
            print(f'Loading {call} at the {colorise(start)} rod', self.expose(), sep='\n')

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
        self.overflow = False
        self.r0.earth.clear()
        self.r0.sky.clear()
        # c50 and c56 are the ones that's actually end up cleared, as the last nxt
        for c in self.val[:-2]:
            nxt = self.val[c.pl + 2]
            exchange(nxt, c)
        self.chk_flow(over=True)
        if verbose:
            print('Moving up', self.expose(), sep='\n')

    def left(self):
        """Moves all cells Down"""
        self.underflow = False
        self.r5.earth.clear()
        self.r5.sky.clear()
        # Similarly to right, c00 and c06 end up cleared
        for c in self.val[:1:-1]:
            nxt = self.val[c.pl - 2]
            exchange(nxt, c)
        self.chk_flow(over=False)
        if verbose:
            print('Moving down', self.expose(), sep='\n')

    def add1(self, addend, cell_0=0):
        """Adds a number to the abacus """
        self.overflow = False
        if verbose:
            print(f'Adding {addend} at the {colorise(cell_0)} rod')
        self.push(self.val[cell_0], addend)
        if verbose:
            self.chk_flow(over=True)
            print(self.expose())

    def sub1(self, subtrahend, cell_0=0):
        """Subtract a number from the abacus"""
        self.underflow = False
        if verbose:
            print(f'subtracting {subtrahend} at the {colorise(cell_0)} rod')
        self.pull(self.val[cell_0], subtrahend)
        if verbose:
            self.chk_flow(over=False)
            print(self.expose())

    def addition(self, augend, *addendi):
        if not augend is None:  # For using former answer
            self.load(augend)
        for a in addendi:
            self.add1(a)

    def subtraction(self, minuend, *subtrahendi):
        if not minuend is None:  # For using former answer
            self.load(minuend)
        for s in subtrahendi:
            self.sub1(s)

    def subfrom1(self, minuend):
        """Subtract the current abacus from a number"""
        self.underflow = False
        if verbose:
            print('subtracting current value from', minuend)
        lngth_subt = self.magnitude()
        minu_start = self.val[lngth_subt * 2]
        self.load(minu_start, minuend)
        for count in range(lngth_subt):
            while self.r0.earth.not_zero():
                consume(self.r0.earth, minu_start)
            while self.r0.sky.not_zero():
                consume(self.r0.sky, self.val[lngth_subt * 2 + 1])
            self.right()
        if verbose:
            self.chk_flow(over=False)
            print(self.expose())

    def multiplication(self, multiplier, multiplicand):
        # Measuring the factors
        self.load(multiplicand)
        lngth_cand = self.magnitude()
        self.load(multiplier)
        lngth_ier = self.magnitude()

        # High edge cases
        if lngth_cand + lngth_ier > 7:
            print(f'Sorry chemp, both {multiplier} and {multiplicand} are too big. '
                  f'Try to have their order of magnitude sum as 7 or less.')
            self.clear()
            return

        # The main operation
        for count in range(lngth_ier):
            while self.r0.earth.not_zero() or self.r0.sky.not_zero():
                self.sub1(1)  # to offer verbose option
                self.add1(multiplicand, cell_0=min(lngth_ier * 2, (6 - lngth_cand) * 2, 10))
            if count < min((6 - lngth_cand), 5):
                self.right()

    def multi_multiplication(self, multplicand, *multiplieri):
        self.multiplication(multiplieri[0], multplicand)
        for m in multiplieri[1:]:
            self.mult1(m)

    def mult1(self, multiplicand):
        """multiply what's in the abacus by another number"""
        lngth = self.magnitude()
        try:
            self.push(self.val[lngth * 2], multiplicand)
        except IndexError:
            self.flow(over=True)
        if self.overflow or self.r5.earth.not_zero() or self.r5.sky.not_zero():
            print(f'Sorry chemp, both previous answer and {multiplicand} were too big. '
                  f'Try to have their order of magnitude sum as 7 or less.')
            self.overflow = False
            return
        self.pull(self.val[lngth * 2], multiplicand)
        for count in range(lngth):
            while self.r0.earth.not_zero() or self.r0.sky.not_zero():
                self.pull(self.r0, 1)
                self.add1(multiplicand, cell_0=lngth * 2)
            self.right()

    def div1(self, divisor):
        """divide what's in the abacus by another number"""
        if divisor == 0:
            print("Abacus catches fire.")
            self.clear(st=True, verbose=False)
            if verbose:
                print(self.expose())
            # we don't want the self description of clear,
            # but we want to print self.expose() whether or not verbose is on.
            return
        lngth_dend = self.magnitude() * 2
        try:
            self.load(divisor, start=lngth_dend)
        except IndexError:
            print('Sorry. You need to leave enough room for both dividend and divisor')
            return
        lngth_sor = (self.magnitude() * 2) - lngth_dend
        self.clear(start=lngth_dend)
        pl = lngth_dend - lngth_sor + 2
        for count in range(pl // 2):
            # pl happen to correspond to number of iterations.
            self.left()
            while not self.underflow:
                self.sub1(divisor, cell_0=pl)
                self.add1(1)
            self.add1(divisor, pl)
            self.sub1(1)
        print(f'Red rod to {colorise(pl - 2)} rod are qutient, '
              f'{colorise(pl)} rod to Violet rod are reminder')


if __name__ == "__main__":
    verbose = True
    abacus = Abacus()
    # abacus.multiplication(24 ** 2, 24 ** 4 - 1)
    # abacus.num_read([4, 2, 0, 0, 5, 3, 5, 3, 5, 3, 5, 1])
    abacus.load(12 * 24 ** 3)
    # abacus.subfrom1(24 ** 2)
    # abacus.div1(2)
    abacus.prnt(tee=not verbose)
    if verbose:
        print("FIN")

"""
TODO: 
num_read dec -> quad-sex
What to do with flow and its check. perheps exception
standardise and managing verbose, perheps make printing and loging into it's own module. or at least make a function for
    verbose.
Done:
fix flow
cli
more rebust solution for length_lier+length_cand = 5
replace length24
how to treat the carry and borrow flags
treat the clear issue
trying to make a function that will actually be more localised to the one beed, 
at the price of running more of them, it will also be more ready to add carry.
will probably want to seperate push and pull anyway"""

"""
rod to write to = lngth + length_cand - 2 (starting at 0)
too big rod = 5
too big lngth = 7 - length_cand
for 0 5
for 1 4
for 2 3
"""
