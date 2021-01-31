data = [0, 0]
program = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)  # length 4x4
PC = 0


def nand(call, operand, back):
    data[back] = int(not (data[call] and operand))


def ifeq0(call, instruct):
    global PC
    if not data[call]:
        PC = instruct - 1


while PC < 5:
    PC4 = PC * 4
    if program[PC4]:
        nand(call=PC4 + 1, operand=PC4 + 2, back=PC4 + 3)
    else:
        ifeq0(call=PC4 + 1, instruct=PC4 + 2 + 2 * (PC4 + 3))
    PC += 1
print(data)