try:
    try:
        print(1/0)
    except ZeroDivisionError:
        print('b')
except ZeroDivisionError:
    print('a')