import sys
from cesar import abc,cesar,check_letters
import re
import collections

regex = re.compile('[^a-zA-Z]')
# etaoinshrdlcumwfgypbvkjxqz
# A dictionary with the relative frequencies of each letter in English
freq_list2 = dict(e=12.702, t=9.056, a=8.167, o=7.507, i=6.966, n=6.749, s=6.327, h=6.094, r=5.987, d=4.253, l = 4.025,
                 c=2.782, u=2.758, m=2.406, w=2.36, f=2.228, g=2.015, y=1.974, p=1.929, b=1.492, v=0.978, k=0.772,
                 j=0.153, x=0.15, q=0.095, z=0.074)
# A dictionary with the relative frequencies of each letter in Latin
freq_list = dict(i=11.44, e=11.38, a=8.69, u=8.46, t=8, s=7.6, r=6.67, n=6.28, o=5.4, m=5.38, c=3.99, l=3.15, p=3.03,
                 d=2.77, b=1.58, q=1.51, g=1.21, v=0.96, f=0.93, h=0.69, x=0.6, y=0.07, z=0.01)


def letter_frequency(text):
    """Returns a dictionary with the relative frequency of each letter, case-insensitive. Ignores non-letters."""
    text = regex.sub('', text.lower())
    n = float(len(text))

    dic = collections.defaultdict(int)
    # absolute frequencies
    for letter in text:
        dic[letter] += 1

    # relative frequencies
    letters_dic = {}
    #for x in ascii_lowercase:
    for x in abc:
        letters_dic[x] = (dic[x] / n) * 100

    return letters_dic


def similarity(deciphered_text, plain_text):

    if len(deciphered_text) != len(plain_text):
        print("Error! Different lengths of texts")
        sys.exit(2)

    # To reduce variance, convert all to lowercase and eliminate non-alphabetic characters
    deciphered_text = regex.sub('', deciphered_text.lower())
    plain_text = regex.sub('', plain_text.lower())

    l2 = len(plain_text)

    differences = 0.0
    for i in xrange(l2):
        if plain_text[i] != deciphered_text[i]:
            differences += 1

    # Return ratio of similarity
    return (l2-differences)/l2

def main():

    if len(sys.argv) != 3:
        print("Usage: ",sys.argv[0]," clar.txt xifrat.txt")
        sys.exit(2)
    try:
        plain_text = open(sys.argv[1]).read()
        ciphertext = open(sys.argv[2]).read()
    except IOError:
        print("Input file not found!")
        sys.exit(2)

    if len(plain_text) != len(ciphertext):
        print("Error: plain and ciphertext have different lengths")
        sys.exit(2)

    # If the texts have some of the forbidden letters
    if check_letters(plain_text) or check_letters(ciphertext):
        sys.exit(2)

    min_dif = 100
    min_i = len(abc) + 1
    for i in xrange(len(abc)):
        dif = 0
        for letter in freq_list:
            # Assume the key is i end try to dechiper.
            possible_plain_text = cesar(ciphertext, -i)
            plaint_freq = letter_frequency(possible_plain_text)
            # Compute the difference of frequencies between the deciphered text and English.
            dif += abs(plaint_freq[letter] - freq_list[letter])
        # Save which has a minimum difference, meaning the most likely key.
        if dif < min_dif:
            min_i = i
            min_dif = dif

    #print "Key: ", min_i
    deciphered_text = cesar(ciphertext, -min_i);
    print("Deciph: ", deciphered_text)
    print("Clar  : ",plain_text)

    if deciphered_text == plain_text:
        print(1)
        sys.exit(1)

    sim = similarity(deciphered_text,plain_text)
    print("Similarity: ",similarity(deciphered_text,plain_text)*100, "%")
    if sim >= 0.8:
        print(1)
        sys.exit(1)
    print(0)
    sys.exit(0)


if __name__ == "__main__":
    main()
