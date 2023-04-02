def whatfor(stuff):
    for s in stuff:
        if s.startswith('x'):
            print(s + 'x')
        else:
            print('x' + s[1:] + s[0])

whatfor(['xero', 'yero', 'yactl', 'y']         )