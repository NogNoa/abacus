help_dscrpt = \
    """
An interactive quad-seximal abacus for fun. 
The Abacus have 12 cells in 6 rods. 
Each rod has a lower cell with 5 beads and a high cell with 3 beads. 
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


def colorise(rod: int) -> str:
    colors = ('Red', 'Yellow', 'Green', 'Blue', 'Indigo', 'Violet')
    return colors[rod]


def exchange(donor, acceptor) -> int:
    back = 0
    while donor.not_zero():
        donor.pull()
        back |= acceptor.push()
    return back


def consume(hybris, nemesis) -> int:
    back = 0
    while hybris.not_zero():
        hybris.pull()
        back |= nemesis.pull()
    return back


class Bead:
    def __init__(self, pl: int, cid: str):
        self.up = False
        self.id = cid + '.b' + str(pl)

    def __str__(self):
        if self.up:
            return 'Up'
        else:
            return 'Down'

    def __repr__(self):
        return self.id

    def __int__(self):
        return int(self.up)

    def push_pull(self, force: int, push: bool) -> int:
        if force < 1:
            return force
        if push == self.up:
            return force
        else:
            self.up = push
            return force - 1


class End:
    def __init__(self, up: bool, cid: str):
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

    # noinspection PyUnusedLocal
    @staticmethod
    def push_pull(force: int, push: bool) -> int:
        return force


class Cell:
    def __init__(self, deck: str, pl: int, rid: str):
        self.id = rid + '.c' + str(pl * 6)  # .c0 or .c6
        self.size = bool(not pl)
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

    def expose(self):
        back = ''
        up = False
        for b in self.val:
            if isinstance(b, End):
                if not b.up:
                    back += '||- '
                else:
                    if not up:
                        back += '--- '
                        back += '--- ' * 2 * self.size
                    back += '-|| '
            elif b.up == up:
                assert isinstance(b, Bead)
                back += '-O- '
            else:
                assert b.up != up
                back += '--- ' + '--- ' * 2 * self.size + '-O- '
                up = True
        return back

    def __str__(self):
        return self.id[3] + '.' + self.deck

    def __repr__(self):
        return str([(str(b), repr(b)) for b in self.val])

    def __int__(self):
        return sum(int(b) for b in self.val)

    def push_pull(self, force: int, push: bool) -> int:
        for b in self.val[::-drc(push)]:
            if not force:
                break
            force = b.push_pull(force, push)
        # force = self.val[push * -1 - drc(push)].push_pull(force, push)
        # push * -1 - drc(push) == {0,1} * -1 - drc({0,1}) = {0,-1} - {-1,1) = {1,-2}
        # We pass the operation to bottom of the cell if pull (0 * -1 --1 = 1, first in cell) or to top if push
        # (1 * -1 - 1 = -2, last in cell). For each bead moved force will go down by 1, and the new value
        # will be returned here.
        return force

    def push(self, force=1):
        """Move beads in a given cell to the Right"""
        self.push_pull(force, push=True)

    def pull(self, force=1):
        """Return beads in a given cell to the Left"""
        self.push_pull(force, push=False)

    def set_clear(self, st: bool):
        for b in self.val[1:-1]:
            b.up = st  # true->set false->clear

    def set(self):
        """Move all beads in a given cell to the Right"""
        self.set_clear(st=True)

    def clear(self):
        """Return all beads in a given cell to the Left, reseting it to Zero."""
        self.set_clear(st=False)

    def load(self, const: int):
        """Set a given cell to a speicific number."""
        self.clear()
        self.push(const)

    def not_zero(self) -> bool:
        return self.val[-2].up

    def not_full(self) -> bool:
        return not self.val[1].up

    def not_zero_full(self, push: bool) -> bool:
        if push:
            return self.not_full()
        else:
            return self.not_zero()


class Rod:
    def __init__(self, pl: int, color: str):
        self.id = 'r' + str(pl)
        self.color = color

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

    def quad_sex(self) -> str:
        """Has nothing to do with foursomes"""
        return str(int(self.sky)) + str(int(self.earth))

    def expose(self) -> str:
        back = self.earth.expose() + self.sky.expose()
        back += self.color + '\n'
        return back

    def set_clear(self, st=False):
        self.earth.set_clear(st)
        self.sky.set_clear(st)

    def push_pull(self, force: int, push: bool) -> int:
        force = self.earth.push_pull(force, push)
        if force:
            sky_already_done = self.sky.push_pull(1, push)
            self.earth.set_clear(st=not push)
            if sky_already_done:
                self.sky.set_clear(st=not push)
                # we are returning the force as is, the rest of carry/borrow
                # as well as subtracting 1 from force is handled by abacus.
            else:
                force = self.push_pull(force - 1, push)
        return force

    def push_pull2(self, cell: Cell, force: int, push: bool) -> int:
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

    def push(self, force: int = 1):
        return self.push_pull(force, True)

    def pull(self, force: int = 1):
        return self.push_pull(force, False)

    def clear(self):
        self.earth.clear()
        self.sky.clear()

    def not_zero(self) -> bool:
        return self.earth.not_zero() or self.sky.not_zero()

    def load(self, const: int):
        self.clear()
        self.push_pull(const, True)


class Abacus:
    def __init__(self):
        self.r0 = Rod(0, colorise(0))
        self.r1 = Rod(1, colorise(1))
        self.r2 = Rod(2, colorise(2))
        self.r3 = Rod(3, colorise(3))
        self.r4 = Rod(4, colorise(4))
        self.r5 = Rod(5, colorise(5))
        self.val = (self.r0, self.r1, self.r2, self.r3, self.r4, self.r5,)
        self.overflow = False
        self.underflow = False

    def __repr__(self):
        return str([(r.quad_sex(), str(r)) for r in self.val])

    def __int__(self):
        return self.num_print(5)

    def quad_sex(self) -> str:
        return ':'.join(r.quad_sex() for r in self.val)

    def expose(self) -> str:
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

    def num_read(self, call: list):
        for pl, num in enumerate(call):
            self.val[pl].load(num)

    def num_print(self, *args: int):
        if len(args) == 0:
            args = (5,)
            rod_0 = 0
        elif len(args) == 1:
            rod_0 = 0
        else:  # if len(args) >= 2:
            rod_0 = args[0]
        return sum(int(self.val[r]) * 24 ** (r - rod_0) for r in range(*args))

    def flow(self, over: bool):
        if over:
            self.overflow = True
        else:
            self.underflow = True

    def chk_flow(self, over: bool):
        if over:
            flow = self.overflow
            word = 'overflowed'
        else:
            flow = self.underflow
            word = 'underflowed'
        if flow:
            print(f"I got {word}\n")

    def push_pull(self, rod_ind: int, force: int, push: bool):
        if force >= 24 ** 6:
            print(f'\nVery funny. The input {force} is too big for my brain. '
                  f'I\'m not wasting my time. Try {24 ** 6 - 1} max.\n')
            self.flow(over=push)  # push -> overflow; pull -> underflow
            force = 0
            # if the number is higher than what the abacus could hold in the first place,
            # we set the respective flow flag, and empty the force so the operation will finish
            # wherever control is returned to.
        rod = self.val[rod_ind]
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
                self.push_pull(rod_ind + 1, 1, push)
                # For most cells we pass a carry of 1 to the next cell
            else:
                self.flow(over=push)
                # But if it is the last cell we have to flag the corresponding flow flag instead.
            rod.set_clear(st=not push)  # push-> set, pull-> clear
            force = rod.push_pull(force - 1, push)
            # Then we set or clear the cell and pass a push or pull command to the ends as before.
            # We subtract 1 force to pay for the set/clear. We continue the loop until force is zero.

    def push(self, rod=0, force=1):
        """Move beads in a given cell to the Right"""
        self.push_pull(rod, force, push=True, )

    def pull(self, rod=0, force=1):
        """Return beads in a given cell to the Left"""
        self.push_pull(rod, force, push=False)

    def set_clear(self, st=False, start=0, verbose=verbose, fromhigh=False):
        """Clear every Cell of the abacus"""
        if fromhigh:
            #  To start from the upper cell of a rod
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

    def set(self, start=0, verbose=verbose, fromhigh=False):
        self.set_clear(True, start, verbose, fromhigh)

    def clear(self, start=0, verbose=verbose, fromhigh=False):
        self.set_clear(False, start, verbose, fromhigh)

    def load(self, call: int, start=0):
        """Set the abacus to a specific number"""
        self.overflow = False
        self.clear(verbose=False, start=start)
        # clears length-1 cells, starting from the one after cell_0. cell_0 will already be cleared by load()
        self.push(start, call)
        self.chk_flow(over=True)
        if verbose:
            print(f'Loading {call} at the {colorise(start)} rod', self.expose(), sep='\n')

    def _fast_load(self, call: int):
        for rod in self.val:
            rod.load(call % 24)
            call //= 24

    def magnitude(self) -> int:
        if self.overflow:
            return 7
        if self.underflow:
            return -1
        for back in range(6, -1, -1):
            icositetrigit = self.val[back - 1].not_zero()  # base 24 digit
            if icositetrigit:
                break
        if verbose:
            # noinspection PyUnboundLocalVariable
            print(f'Mesuring the base-24 order of magnitude of loaded value as {back}\n')
        return back

    def right(self) -> int:
        """Moves all rods right"""
        self.overflow = False
        back = int(self.r0)
        self.r0.clear()
        # r5 is the one that's actually end up cleared, as the last nxt
        for r in range(5):
            curr, nxt = self.val[r], self.val[r + 1]
            exchange(nxt, curr)
        self.chk_flow(over=True)
        if verbose:
            print('Moving up', self.expose(), sep='\n')
        return back

    def left(self) -> int:
        """Moves all rod left"""
        self.underflow = False
        back = int(self.r5)
        self.r5.clear()
        # Similarly to right, c0 end up cleared
        for r in range(5, 0, -1):
            curr, nxt = self.val[r], self.val[r - 1]
            exchange(nxt, curr)
        self.chk_flow(over=False)
        if verbose:
            print('Moving down', self.expose(), sep='\n')
        return back

    def mutual_consume(self, hybris: int, nemesis: int):
        lngth = abs(nemesis-hybris)
        hybris = self.val[hybris]
        nemesis = self.val[nemesis]
        for count in range(lngth):
            borrow = consume(hybris, nemesis)
            self.right()
            if borrow:
                nemesis.pull()


class Human:
    def __init__(self, abacus: Abacus):
        self.abacus = abacus

    def add1(self, addend: int, rod_0=0):
        """Adds a number to the abacus """
        self.abacus.overflow = False
        if verbose:
            print(f'Adding {addend} at the {colorise(rod_0)} rod')
        self.abacus.push(rod_0, addend)
        if verbose:
            self.abacus.chk_flow(over=True)
            print(self.abacus.expose())

    def sub1(self, subtrahend: int, rod_0=0):
        """Subtract a number from the abacus"""
        self.abacus.underflow = False
        if verbose:
            print(f'subtracting {subtrahend} at the {colorise(rod_0)} rod')
        self.abacus.pull(rod_0, subtrahend)
        if verbose:
            self.abacus.chk_flow(over=False)
            print(self.abacus.expose())

    def addition(self, augend: int, *addendi: int):
        if augend is not None:  # For using former answer
            self.abacus.load(augend)
        for a in addendi:
            self.add1(a)

    def subtraction(self, minuend: int, *subtrahendi: int):
        if minuend is not None:  # For using former answer
            self.abacus.load(minuend)
        for s in subtrahendi:
            self.sub1(s)

    def subfrom1(self, minuend: int):
        """Subtract the current abacus from a number"""
        self.abacus.underflow = False
        if verbose:
            print('subtracting current value from', minuend)
        lngth_subt = self.abacus.magnitude()
        self.abacus.load(minuend, lngth_subt)
        self.abacus.mutual_consume(0, lngth_subt)
        if verbose:
            self.abacus.chk_flow(over=False)
            print(self.abacus.expose())

    def multiplication(self, multiplier: int, multiplicand: int):
        # Measuring the factors
        self.abacus._fast_load(multiplicand)
        lngth_cand = self.abacus.magnitude()
        self.abacus._fast_load(multiplier)
        lngth_ier = self.abacus.magnitude()

        # zero edge case
        if not lngth_cand:
            self.abacus.clear()
            return

        # High edge cases
        if lngth_cand + lngth_ier > 5:
            print(f'Sorry chemp, both {multiplier} and {multiplicand} are too big. '
                  f'Try to have their order of magnitude sum as 5 or less.')
            self.abacus.clear()
            return

        if lngth_cand < lngth_ier:
            self.abacus.load(multiplicand)
            multiplicand = multiplier
            lngth_cand, lngth_ier = lngth_ier, lngth_cand

        # The main operation
        for count in range(lngth_ier):
            while self.abacus.r0.not_zero():
                self.sub1(1)  # to offer verbose option
                self.add1(multiplicand, rod_0=lngth_ier)
            self.abacus.right()
        if verbose:
            print("Done")

    def multi_multiplication(self, multplicand: int, *multiplieri: int):
        self.multiplication(multiplieri[0], multplicand)
        for m in multiplieri[1:]:
            self.mult1(m)
        if verbose:
            print("Done all of 'em!")

    def mult1(self, multiplicand: int):
        """multiply what's in the abacus by another number"""
        lngth = self.abacus.magnitude()
        try:
            self.abacus.push(lngth, multiplicand)
        except IndexError:
            self.abacus.flow(over=True)
        if self.abacus.overflow or self.abacus.magnitude() >= 6:
            print(f'Sorry chemp, both previous answer and {multiplicand} were too big. '
                  f'Try to have their order of magnitude sum as 7 or less.')
            self.abacus.overflow = False
            return
        self.abacus.pull(lngth, multiplicand)
        for count in range(lngth):
            while self.abacus.r0.not_zero():
                self.abacus.pull(force=1)
                self.add1(multiplicand, rod_0=lngth)
            self.abacus.right()
        if verbose:
            print("Done")

    def div1(self, divisor: int):
        """divide what's in the abacus by another number"""
        if divisor == 0:
            print("Abacus catches fire.")
            self.abacus.clear(verbose=False)
            if verbose:
                print(self.abacus.expose())
            # we don't want the self description of clear,
            # but we want to print self.expose() whether or not verbose is on.
            return
        lngth_dend = self.abacus.magnitude()
        try:
            self.abacus.load(divisor, start=lngth_dend)
        except IndexError:
            print('Sorry. You need to leave enough room for both dividend and divisor')
            return
        lngth_sor = (self.abacus.magnitude()) - lngth_dend
        self.abacus.clear(start=lngth_dend)
        pl = lngth_dend - lngth_sor + 1
        for count in range(pl):
            # pl happen to correspond to number of iterations.
            self.abacus.left()
            while not self.abacus.underflow:
                self.sub1(divisor, rod_0=pl)
                self.add1(1)
            self.add1(divisor, pl)
            self.sub1(1)
        print(f'Red rod to {colorise(pl - 1)} rod are qutient, '
              f'{colorise(pl)} rod to Violet rod are reminder')
        return pl


# TODO: num_read dec -> quad-sex
#       What to do with flow and its check. mayhaps exception
#       standardise and managing verbose, perhaps make printing and logging into it's own module.
#       or at least make a function for verbose.
#       add operator built-in functions (__add__ etc)
#
"""
Done:
fix flow
cli
more rebust solution for length_lier+length_cand = 5
replace length24
how to treat the carry and borrow flags
treat the clear issue
trying to make a function that will actually be more localised to the one bead, 
at the price of running more of them, it will also be more ready to add carry.
will probably want to seperate push and pull anyway
add rod to hierarchy
separate Abacus to one additional level of abstraction. The highest- Human/Operator/User.
"""
"""
rod to write to = lngth + length_cand - 2 (starting at 0)
too big rod = 5
too big lngth = 7 - length_cand
for 0 5
for 1 4
for 2 3
"""
