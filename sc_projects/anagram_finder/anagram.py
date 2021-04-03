"""
File: anagram.py
Name: CY
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop

# Global variables
dict_lst = []


def main():
    read_dictionary()
    print('Welcome to stanCode "Anagram Generator" (or -1 to quit)')
    while True:
        word = input('Find anagrams for: ')
        if word == EXIT:
            break
        else:
            anagrams = find_anagrams(word)
            print(f'{len(anagrams)} anagrams: {anagrams}')


def read_dictionary():
    with open(FILE, 'r') as f:
        for line in f:
            # get line[:-1] to deal with \n
            dict_lst.append(line[:-1])


def find_anagrams(s):
    """
    :param s: string, the input word to find anagrams
    :return: list, the results of all anagrams
    """
    s_index = []        # Get index for every letter of input word
    ans_lst = []        # To save all anagrams
    distinct_lst = []   # To save distinct letters of the input word
    current_dict = []   # To save words in the dictionary beginning with the letters of the input word
    for i in range(len(s)):
        s_index.append(i)
        if s[i] not in distinct_lst:
            distinct_lst.append(s[i])
            # decrease the words of dictionary to be found
            dict_prefix(s[i], current_dict)
    find_anagrams_helper(s, s_index, [], ans_lst, current_dict)
    return ans_lst


def find_anagrams_helper(s, s_index, current, ans_lst, current_dict):
    """
    :param s: string, the input word to find anagrams
    :param s_index: list, index for every letter of input word
    :param current: list, the part of permutation of index
    :param ans_lst: list, the results of all anagrams
    :param current_dict: list, a list to save words beginning with the letters of the input word
    """
    s_permutations = ''
    # Base case
    if len(current) == len(s_index):
        # Use index to get word
        for i in current:
            s_permutations += s[i]
        # Check the word is not repeated and exists in the dictionary
        if s_permutations not in ans_lst and s_permutations in current_dict:
            ans_lst.append(s_permutations)
            print('Searching...')
            print('Found: '+s_permutations)
    else:
        for num in s_index:
            if num not in current:
                current.append(num)
                sub_s = ''
                for i in current:
                    sub_s += s[i]
                # If there are some words begin with sub_s then continue the recursion
                if has_prefix(sub_s, current_dict):
                    find_anagrams_helper(s, s_index, current, ans_lst, current_dict)
                current.pop()


def has_prefix(sub_s, current_dict):
    """
    :param sub_s: string, part of the input word
    :param current_dict: list, a list to save words beginning with the letters of the input word
    :return: boolean
    """
    cnt = 0
    for w in current_dict:
        if w.startswith(sub_s):
            cnt += 1
    # cnt > 0 means sub_s is a prefix of some words in the dictionary
    return cnt > 0


def dict_prefix(letter, current_dict):
    """
    To decrease the numbers of words in dictionary
    :param letter: str, the beginning letter of the input word
    :param current_dict: list, a list to save words beginning with the letters of the input word
    """
    for w in dict_lst:
        if w.startswith(letter):
            current_dict.append(w)


if __name__ == '__main__':
    main()
