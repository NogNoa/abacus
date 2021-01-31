data = [0, 0]
# we assume data IS cleared at the beginning or no deterministic program will be possible
prog = (1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1)  # length 4x4
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


while PC < 4:
    PC4 = PC * 4
    if prog[PC4]:
        nand(call=prog[PC4 + 1], operand=prog[PC4 + 2], back=prog[PC4 + 3])
    else:
        ifeq0(call=prog[PC4 + 1], instruct=PC4 + 2 + 2 * (PC4 + 3))
print(data)

# 4 is fine, in hardware it whold notice a roll over, that's why I can't allow -1 to happen, and so incrementing
# the PC appears twice when it could otherwisw have appeared once.
