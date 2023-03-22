def set_lowercase(strings):
    """Lower list"""
    for n in range(len(strings)):
        strings[n] = strings[n].lower()



words = ['Right', 'SAID', 'Fred']
set_lowercase(words)
print(words)