def make_tags(tag, word):
    """Tags"""
    first = f'<{tag}>'
    last = f'</{tag}>'
    return first + word + last