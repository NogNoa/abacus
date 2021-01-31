data = [0, 0]
program = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)  # length 4x4
PC = 0


def nand(call, operand, back):
    global PC
    data[back] = int(not (data[call] and operand))
    PC += 1


def ifeq0(call, instruct):
    global PC
    if not data[call]:
        PC = instruct
    else:
        PC += 1


while PC < 5:
    PC4 = PC * 4
    if program[PC4]:
        nand(call=PC4 + 1, operand=PC4 + 2, back=PC4 + 3)
    else:
        ifeq0(call=PC4 + 1, instruct=PC4 + 2 + 2 * (PC4 + 3))
print(data)

# 5 is fine, in hardware it whold notice a roll over, that's why I can't allow -1 to happen, and so incrementing
# the PC appears twice when it could otherwisw have appeared once.
