"""
File: hangman.py
Name: CY
-----------------------------
This program plays hangman game.
Users sees a dashed word, trying to
correctly figure the un-dashed word out
by inputting one character each round.
If the user input is correct, show the
updated word on console. Players have N_TURNS
chances to try and win this game.
"""


import random


# This constant controls how many times players can guess, must >= 6 (There are 6 parts in hangman)
N_TURNS = 7


def main():
    """
    Running the word guessing game
    """
    ans = random_word()
    run_game(ans, N_TURNS)


def run_game(ans, n):
    """
    Players input a character each round, check the guessed character is correct or not up to n times
    :param ans: str, the answer of the game
    :param n: number of chances to try
    """
    # transform to upper case to be case-insensitive
    ans = ans.upper()
    wrong_times = 0
    dashed = ""
    for i in range(len(ans)):
        dashed += '-'
    print_hangman(n, wrong_times)
    print('The word looks like: ' + dashed)
    print('You have '+str(n-wrong_times)+' guesses left.')
    while True:
        input_ch = input('Your guess: ')
        # check type of the input, just only one alphabet can be accepted
        if not (input_ch.isalpha() and (len(input_ch) == 1)):
            print('illegal format.')
        else:
            # transform to upper case to be case-insensitive
            input_ch = input_ch.upper()
            # if guessed alphabet was in the answer word
            if ans.find(input_ch) != -1:
                # check the alphabet's index in the word
                for i in range(len(ans)):
                    if ans[i] == input_ch:
                        # replace the guessed alphabet in the dashed string to show
                        dashed = dashed[:i]+ans[i]+dashed[i+1:]
                print_hangman(n, wrong_times)
                print('You are correct!')
                # if alphabets were not all guessed, the while loop will be continued
                if not dashed.isalpha():
                    print('The word looks like: ' + dashed)
                    print('You have ' + str(n - wrong_times) + ' guesses left.')
                # if all alphabets were guessed, the game is over
                else:
                    print('You win!')
                    print('The word was: ' + ans)
                    break
            # if guessed alphabet wasn't in the answer word
            else:
                wrong_times += 1
                # if wrong times haven't reached N_TURNS, the while loop will be continued
                print_hangman(n, wrong_times)
                if wrong_times < n:
                    print("There's no " + input_ch + "'s in the word.")
                    print('The word looks like: ' + dashed)
                    print('You have ' + str(n - wrong_times) + ' guesses left.')
                # if user guessed the wrong alphabet at the last time, the game is over
                elif wrong_times == n:
                    print("There's no " + input_ch + "'s in the word.")
                    print('You are completely hung :(')
                    print('The word was: ' + ans)
                    break


def print_hangman(n, wrong_times):
    """
    print hangman depends on wrong times
    :param n: int, number of chances to try
    :param wrong_times: int, numbers of guessing the wrong characters
    """
    # the width of the print, must > 4
    width = 13
    height = n
    s = ""
    # let s be a width * height string then we can replace every hangman part each wrong time
    for i in range(height):
        for j in range(width-1):
            s += " "
        # every (width-1) spaces plus a \n to change row
        s += '\n'
    # ceiling
    for i in range(len(s)):
        if i < width-1:
            s = s[:i] + '-' + s[i+1:]
    # pillar and rope
    for i in range(width, len(s), width):
        s = s[:i] + '|' + s[i+1:]
    s = s[:int(width + width/2)] + '|' + s[int(width + width/2 + 1):]
    # head
    if wrong_times >= 1:
        s = s[:int(width*2 + width/2)] + 'O' + s[int(width*2 + width/2 + 1):]
    # body
    if wrong_times >= 2:
        s = s[:int(width*3 + width/2)] + '|' + s[int(width*3 + width/2 + 1):]
    # left hand
    if wrong_times >= 3:
        s = s[:int(width*3 + width/2 - 1)] + '/' + s[int(width*3 + width/2):]
    # right hand
    if wrong_times >= 4:
        s = s[:int(width*3 + width/2 + 1)] + '\\' + s[int(width*3 + width/2 + 2):]
    # if n > 6 continue adding body part until left 2 chances to try
    if (wrong_times >= 5) & (n - wrong_times <= n-5):
        if n - wrong_times > 1:
            # 4 means head, body, left hand and right hand
            for i in range(wrong_times - 4):
                s = s[:int(width * (3+i+1) + width/2)] + '|' + s[int(width * (3+i+1) + width/2 + 1):]
        if n - wrong_times <= 1:
            # 6 means head, body, left hand, right hand, left leg and right leg
            for i in range(n - 6):
                s = s[:int(width * (3+i+1) + width/2)] + '|' + s[int(width * (3+i+1) + width/2 + 1):]
    # left leg
    if n - wrong_times <= 1:
        s = s[:int(width * (height-2) + width/2 - 1)] + '/' + s[int(width * (height-2) + width/2):]
    # right leg
    if n - wrong_times <= 0:
        s = s[:int(width * (height-2) + width/2 + 1)] + '\\' + s[int(width * (height-2) + width/2 + 2):]
    print(s)


def random_word():
    num = random.choice(range(9))
    if num == 0:
        return "NOTORIOUS"
    elif num == 1:
        return "GLAMOROUS"
    elif num == 2:
        return "CAUTIOUS"
    elif num == 3:
        return "DEMOCRACY"
    elif num == 4:
        return "BOYCOTT"
    elif num == 5:
        return "ENTHUSIASTIC"
    elif num == 6:
        return "HOSPITALITY"
    elif num == 7:
        return "BUNDLE"
    elif num == 8:
        return "REFUND"


if __name__ == '__main__':
    main()
