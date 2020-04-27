try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans



# The latin alphabet, without j, k, and w
abc = 'abcdefghilmnopqrstuvxyz'
forbidden_letters = 'jkwJKW'


def check_letters(text):
    for letter in forbidden_letters:
        if letter in text:
            #print "Error! input text contains ", letter, ", which is not in the alphabet"
            return 1
    return 0


def cesar(text, key):
    """Returns a lowercase cipher/plain text, depending if key is positive or negative. Ignores non-letters."""
    key_trans = ''
    if check_letters(text):
        return None

    for letter in abc:
        key_trans += abc[(abc.index(letter) + key) % len(abc)]

    trans = maketrans(abc + abc.upper(), key_trans + key_trans.upper())
    return text.translate(trans)


