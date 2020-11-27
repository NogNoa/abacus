def table_num_listise(table='abacus.csv'):
    call = open(table, 'r+')
    call = call.readlines()
    call = [pl.split(',') for pl in call]
    """
    for i in call:
        i = [pl == '•' for pl in i]
    """
    back = []
    for line in call:
        up = False
        high = False
        i, j = 0, 0
        for pl in line:
            if pl == '---':
                up = True
            if pl == '-||':
                high = True
                up = False
            if pl == '-O-' and up:
                if not high:
                    i += 1
                else:
                    j += 1
        back += (i, j)
    return back



print(table_num_listise())
