help_dscrpt = \
    """
An interactive quad-seximal abacus for fun.\t\n
The Abacus have 12 rods in 6 rows.\t\n
Each row has a lower rod with 5 beeds and a high rod with 3 beeds.\t\n
When the rod is full this is a distinct state, only when you add one to it does the next rod change 
    and the first one empties.\t\n
This make the abacus base 24 by row.\t\n
\t\n
Enter values as base 24 [0123456789abcdefghijklmn] \t\n
If you want to use base 10, that's still an option! \t\n
Enter row by color ['Red', 'Yellow', 'Green', 'Blue', 'Indigo', "Violet"]\t\n
If both inputs are required always enter value before row
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
        self.rod = []
        self.pl = 0

    def expose(self):
        if self.up:
            return 'Up'
        else:
            return 'Down'

    def push_pull(self, force: int, push: bool):
        if force < 1:
            return force
        rod, pl = self.rod, self.pl
        dr = - 1 + (2 * push)  # direction push = +1 pull = -1
        if self.up != rod[pl + dr].up:
            self.up = not self.up
            force -= 1
        force = rod[pl - dr].push_pull(force, push)
        return force


class End:
    def __init__(self, up):
        self.up = up
        self.id = 'end'
        self.rod = []
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
            # only does work in the right direction, when reaching the other end it returns to the rod
            rod, pl = self.rod, self.pl
            dr = - 1 + (2 * push)  # direction push = +1 pull = -1
            force = rod[pl - dr].push_pull(force, push)
        return force


class Rod:
    def __init__(self, size, cid, color):
        self.id = cid
        self.size = (size == 'big')
        self.color = color
        self.abacus = []
        self.pl = 0

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
            b.rod, b.pl = initorder(b, self)

    def expose(self):
        return [(i.expose(), i.id) for i in self.val]

    def push_pull(self, force, push):
        force = self.val[push * -1].push_pull(force, push)
        # We pass the operation to bottom of the rod if pull (0 * -1 = 0, first in rod) or to top if push
        # (1 * -1 = -1, last in rod). For each beed moved force will go down by 1, and the new value
        # will be returned here.
        return force

    def push(self, force=1):
        """Move beeds in a given rod to the Right"""
        self.push_pull(force, push=True)

    def pull(self, force=1):
        """Return beeds in a given rod to the Left"""
        self.push_pull(force, push=False)

    def set_clear(self, st: bool):
        for b in self.val[1:-1]:
            b.up = st  # true->set false->clear

    def set(self):
        """Move all beeds in a given rod to the Right"""
        self.set_clear(st=True)

    def clear(self):
        """Return all beeds in a given rod to the Left, reseting it to Zero."""
        self.set_clear(st=False)

    def load(self, const):
        """Set a given rod to a speicific number."""
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


def exchange(donor, acceptor):
    while donor.not_zero():
        donor.pull()
        acceptor.push()


def consume(hybris, nemesis):
    while hybris.not_zero():
        hybris.pull()
        nemesis.pull()


class Abacus:
    def __init__(self):
        self.c00 = Rod('big', 'c00', 'Red',)
        self.c06 = Rod('small', 'c06', 'Red',)
        self.c10 = Rod('big', 'c10', 'Yellow',)
        self.c16 = Rod('small', 'c16', 'Yellow',)
        self.c20 = Rod('big', 'c20', 'Green',)
        self.c26 = Rod('small', 'c26', 'Green',)
        self.c30 = Rod('big', 'c30', 'Blue',)
        self.c36 = Rod('small', 'c36', 'Blue',)
        self.c40 = Rod('big', 'c40', 'Indigo',)
        self.c46 = Rod('small', 'c46', 'Indigo',)
        self.c50 = Rod('big', 'c50', 'Violet',)
        self.c56 = Rod('small', 'c56', 'Violet',)
        self.val = (self.c00, self.c06, self.c10, self.c16, self.c20, self.c26,
                    self.c30, self.c36, self.c40, self.c46, self.c50, self.c56)
        for c in self.val:
            c.abacus, c.pl = initorder(c, self)
        self.major = [c for c in self.val[::2]]
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
            self.flow(over=push)
            force = 0
            # if the number is higher than what the abacus could hold in the first place,
            # we set the respective flow flag, and empty the force so the operation will finish
            # wherever control is returned to.
        force = rod.push_pull(force, push)
        while force > 0:
            if push and rod.not_full():
                print('Error! I tried to carry while rod is not full')
            elif (not push) and rod.not_zero():
                print('Error! I tried to borrow while rod is not empty')
            # If we got here it means the force was bigger than the number of beeds that were down.
            if rod.id != 'c56':
                self.push_pull(self.val[rod.pl + 1], 1, push)
                # For most rods we pass a carry of 1 to the next rod
            else:
                self.flow(over=push)
                # But if it is the last rod we have to flag the corresponding flow flag instead.
            rod.set_clear(st=not push)  # push-> set, pull-> clear
            force = rod.push_pull(force - 1, push)
            # Then we set or clear the rod and pass a push or pull command to the ends as before.
            # We substruct 1 force to pay for the set/clear. We continue the loop until force is zero.

    def push(self, rod: Rod, force=1):
        """Move beeds in a given rod to the Right"""
        self.push_pull(rod, force, push=True,)

    def pull(self, rod: Rod, force=1):
        """Return beeds in a given rod to the Left"""
        self.push_pull(rod, force, push=False)

    def clear(self, reverse=False, start=0, verbose=verbose):
        """Clear every Rod of the abacus"""
        for c in self.val[start:]:
            c.set_clear(reverse)
        if verbose:
            if reverse:
                print(f'Setting all from row {int(start / 2)}')
            else:
                print(f'Clearing all from row {int(start / 2)}')
            print(self.expose())

    # note, making a macro for set is superfluous. But it's implemented by Truing reverse.

    def load(self, call, start=0):
        """Set the abacus to a specific number"""
        self.overflow = False
        self.clear(verbose=False, start=start)
        # clears lngth-1 rods, starting from the one after rod_0. rod_0 will already be cleared by load()
        self.push(self.val[start], call)
        self.chk_flow(over=True)
        if verbose:
            print(f'Loading {call} at row {int(start / 2)}', self.expose(), sep='\n')

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
        """Moves all rods Up"""
        self.overflow = False
        self.c00.clear()
        self.c06.clear()
        # c50 and c56 are the ones that's actually end up cleared, as the last nxt
        for c in self.val[:-2]:
            nxt = self.val[c.pl + 2]
            exchange(nxt, c)
        self.chk_flow(over=True)
        if verbose:
            print('Moving up', self.expose(), sep='\n')

    def left(self):
        """Moves all rods Down"""
        self.underflow = False
        self.c50.clear()
        self.c56.clear()
        # Similarly to right, c00 and c06 end up cleared
        for c in self.val[:1:-1]:
            nxt = self.val[c.pl - 2]
            exchange(nxt, c)
        self.chk_flow(over=False)
        if verbose:
            print('Moving down', self.expose(), sep='\n')

    def add1(self, addend, rod_0=0):
        """Adds a number to the abacus """
        self.overflow = False
        if verbose:
            print(f'Adding {addend} at row {int(rod_0 / 2)}')
        self.push(self.val[rod_0], addend)
        self.chk_flow(over=True)
        if verbose:
            print(self.expose())

    def sub1(self, subtrahend, rod_0=0):
        """Subtract a number from the abacus"""
        if verbose:
            print(f'subtracting {subtrahend} at row {int(rod_0 / 2)}')
        self.pull(self.val[rod_0], subtrahend)
        self.chk_flow(over=False)
        if verbose:
            print(self.expose())

    def addition(self, augend, *addendi):
        if not augend is None:  # For useing former answer
            self.load(augend)
        for a in addendi:
            self.add1(a)

    def subtraction(self, minuend, *subtrahendi):
        if not minuend is None:  # For useing former answer
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
            while self.c00.not_zero():
                consume(self.c00, minu_start)
            while self.c06.not_zero():
                consume(self.c06, self.val[lngth_subt * 2 + 1])
            self.right()
        self.chk_flow(over=False)
        if verbose:
            print(self.expose())

    def multiplication(self, multiplier, multiplicand):
        # Mesuring the factors
        self.overflow = False
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
            while self.c00.not_zero() or self.c06.not_zero():
                self.sub1(1)  # to offer verbose option
                self.add1(multiplicand, rod_0=min(lngth_ier * 2, (6 - lngth_cand) * 2, 10))
            if count < min((6 - lngth_cand), 5):
                self.right()
        self.chk_flow(over=True)

    def multi_multiplication(self, multplicand, *multiplieri):
        self.multiplication(multiplieri[0], multplicand)
        for m in multiplieri[1:]:
            self.mult1(m)

    def mult1(self, multiplicand):
        """multiply what's in the abacus by another number"""
        self.overflow = False
        lngth = self.magnitude()
        try:
            self.push(self.val[lngth * 2], multiplicand)
        except IndexError:
            self.flow(over=True)
        if self.overflow or self.c50.not_zero() or self.c56.not_zero():
            print(f'Sorry chemp, both previous answer and {multiplicand} were too big. '
                  f'Try to have their order of magnitude sum as 7 or less.')
            self.overflow = False
            return
        self.pull(self.val[lngth * 2], multiplicand)
        for count in range(lngth):
            while self.c00.not_zero() or self.c06.not_zero():
                self.pull(self.c00, 1)
                self.add1(multiplicand, rod_0=lngth * 2)
            self.right()
        self.chk_flow(over=True)

    def div1(self, divisor):
        """divide what's in the abacus by another number"""
        if divisor == 0:
            print("Abacus catches fire.")
            self.clear(reverse=True, verbose=False)
            if verbose:
                print(self.expose())
            # we don't want the self description of clear,
            # but we want to print self.expose() wheter or not verbose is on.
            return
        lngth_dend = self.magnitude() * 2
        self.load(divisor, start=lngth_dend)
        lngth_sor = (self.magnitude() * 2) - lngth_dend
        self.clear(start=lngth_dend)
        pl = lngth_dend - lngth_sor + 2
        for count in range(lngth_dend - lngth_sor):
            self.left()
            while not self.underflow:
                self.sub1(divisor, rod_0=pl)
                self.add1(1)
            self.push(self.val[pl], divisor)
            self.sub1(1)
        print(f'Red row to {self.val[pl - 2].color} row are qutient, '
              f'{self.val[pl].color} row to Violet row are reminder')


if __name__ == "__main__":
    verbose = True
    abacus = Abacus()
    # abacus.multiplication(24 ** 2, 24 ** 4 - 1)
    # abacus.num_read([4, 2, 0, 0, 5, 3, 5, 3, 5, 3, 5, 1]
    abacus.load(24)
    # abacus.subfrom1(24 ** 2)
    abacus.div1(5)
    abacus.prnt(tee=not verbose)
    if verbose:
        print("FIN")

"""
TODO: 
standardise and managing verbose
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
row to write to = lngth + length_cand - 2 (starting at 0)
too big row = 5
too big lngth = 7 - length_cand
for 0 5
for 1 4
for 2 3
"""
