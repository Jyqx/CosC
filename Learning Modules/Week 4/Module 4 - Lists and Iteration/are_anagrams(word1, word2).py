def are_anagrams(word1, word2):
    """Checks for anagrams"""
    return list.sort((word1)) == list.sort((word2)) 