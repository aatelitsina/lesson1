def get_summ(one, two, delimeter=' '):
    result = str(one) + str(delimeter) + str(two)
    return result.upper()

print(get_summ('Hello', 'world!'))
