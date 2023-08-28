def change_middle(word):
    """Change middle 2 characters"""
    data = list(word)
    mid = len(data) / 2
    mid_char = data[mid-1:mid+1]
    print(mid_char)

    

change_middle("wordsssss")