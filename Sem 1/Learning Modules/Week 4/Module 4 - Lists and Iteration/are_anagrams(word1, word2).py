def are_anagrams(word1, word2):
    """Checks for anagrams"""
    word1_l = list(word1)
    word2_l = list(word2)
    word1_l.sort()
    word2_l.sort()
    if not word1 == word2:
        return word1_l == word2_l
    else:
        return False

# Uc answer

# def are_anagrams(word1, word2):
#     """True iff word1 is an anagram of word2"""
#     return word1 != word2 and sorted(list(word1)) == sorted(list(word2))