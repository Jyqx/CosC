# My solution

def rhymes(string_1, string_2, syllable):
    """Check for syllable in both words if words are different"""
    if string_1 == string_2:
        return False
    elif syllable in string_1 and syllable in string_2:
        return True
    else:
        return False
    
    # Uc Solution (Proper Way)

    # def rhymes(string_1, string_2, syllable):
    # ''' Return a boolean specifying whether the two strings start 
    #     and end the same, but are different.
    # '''
    # in_string1 = syllable in string_1
    # in_string2 = syllable in string_2
    # all_same = string_1 == string_2
    # return in_string1 and in_string2 and not all_same
