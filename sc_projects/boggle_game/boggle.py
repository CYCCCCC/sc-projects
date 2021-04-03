"""
File: boggle.py
Name: CY
----------------------------------------
This program recursively finds all words created by the entered letters.
"""

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'


# Constants
SIZE = 4           # Control the number of input letters
MIN_NUMBER = 4     # Control the minimum size of word to be found


def main():
	"""
	Recursively finds all words created by the entered letters.
	"""
	check_cnt = 0         # Save the number of rows that entered letters are correct
	current_dict = []     # Save words in the dictionary beginning with the entered letters
	s_lst = []            # Save the entered letters, every row in a list, 4 lists into s_lst
	w_lst = []            # Save the found words
	for i in range(SIZE):
		s = input(f'{i + 1} row of letters: ')
		# Process the input letters and check the formats
		input_check = input_process(s, s_lst)
		if input_check:
			check_cnt += 1    # Every input in a row is correct then count as 1
		else:
			print('Illegal input')
			break
	# All entered letters are correct
	if check_cnt == SIZE:
		# Decrease the words of dictionary to be found
		dict_prefix(s_lst, current_dict)
		find_answers(s_lst, w_lst, current_dict)


def input_process(s, lst):
	"""
	Process the entered letters and check the formats are correct
	:param s: string, the entered letters separated by space
	:param lst: list, the processed result, 4 letters in a list separated by comma, 4 lists in a list
	:return: boolean, the entered letters are correct or not
	"""
	s = s.split()
	# Check there are 4 letters in one row
	if len(s) != SIZE:
		return False
	else:
		# Check every element is only one alphabet
		for i in range(len(s)):
			if len(s[i]) != 1 or not s[i].isalpha():
				return False
		s = list(map(lambda e: e.lower(), s))    # Case insensitive
		lst.append(s)
		return True


def find_answers(s_lst, w_lst, current_dict):
	"""
	Find all words created by entered letters and exist in dictionary
	:param s_lst: list, save the entered letters, 4 letters in a list separated by comma, 4 lists in a list
	:param w_lst: list, save the found words
	:param current_dict: list, save words in the dictionary beginning with the entered letters
	"""
	# Use every entered letter to be the start letter in turn
	for i in range(SIZE):
		for j in range(SIZE):
			w_index = []        # Save the row and column index of the letter
			current = [i, j]    # Current letter to check
			w_index.append(current)
			find_answers_helper(current, w_index, s_lst, w_lst, current_dict)
	print(f'There are {len(w_lst)} words in total.')


def find_answers_helper(current, w_index, s_lst, w_lst, current_dict):
	"""
	:param current: list, with row and column index of current letter like [row, column]
	:param w_index: list, save possible coordinates combination of letters
	:param s_lst: list, save the entered letters, 4 letters in a list separated by comma, 4 lists in a list
	:param w_lst: list, save the found words
	:param current_dict: list, save words in the dictionary beginning with the entered letters
	"""
	row = current[0]
	col = current[1]
	# Use double for loop to get all possible connected coordinates of letters
	for i in range(-1, 2):       # -1, 0, 1 is the range one letter can connect with, both by row and by column
		for j in range(-1, 2):
			# Exclude coordinates out of range
			if 0 <= row+i <= SIZE-1 and 0 <= col+j <= SIZE-1 and [row+i, col+j] not in w_index:

				# Choose
				w_index.append([row+i, col+j])
				current = [row+i, col+j]     # Move current to the connected coordinate to find the next one

				# create the string by the letters at the coordinates
				w = ''
				for k in range(len(w_index)):
					w_row = w_index[k][0]
					w_col = w_index[k][1]
					w += s_lst[w_row][w_col]

				# Explore
				# When there are more than 4 letters in the string
				if len(w_index) >= MIN_NUMBER:
					if w in current_dict:      # Check the string exists in dictionary
						if w not in w_lst:     # Check the string isn't repeated
							w_lst.append(w)    # Get answer
							print(f'Found "{w}"')
						# Go into the next recursion after finding words in the dictionary
						find_answers_helper(current, w_index, s_lst, w_lst, current_dict)
				# When there are less than 4 letters in the string
				else:
					# Check there are some words in dictionary beginning with the string
					if has_prefix(w, current_dict):
						# Go into the next recursion after finding words in the dictionary
						find_answers_helper(current, w_index, s_lst, w_lst, current_dict)

				# Un-choose
				w_index.pop()


def read_dictionary(dict_lst):
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""
	with open(FILE, 'r') as f:
		for line in f:
			dict_lst.append(line[:-1])


def dict_prefix(s_lst, current_dict):
	"""
	Keep words beginning with the entered letters to decrease the numbers of words in dictionary
	:param s_lst: list, save the entered letters, 4 letters in a list separated by comma, 4 lists in a list
	:param current_dict: list, save words in the dictionary beginning with the entered letters
	"""
	dict_lst = []
	distinct_lst = []
	read_dictionary(dict_lst)
	for i in range(SIZE):       # Check every entered letter
		for j in range(SIZE):
			if s_lst[i][j] not in distinct_lst:     # Check the letter isn't repeated
				distinct_lst.append(s_lst[i][j])
				for w in dict_lst:
					if w.startswith(s_lst[i][j]):
						current_dict.append(w)


def has_prefix(sub_s, current_dict):
	"""
	:param sub_s: string, part of the input word
	:param current_dict: list, save words in the dictionary beginning with the entered letters
	:return: boolean
	"""
	cnt = 0
	for w in current_dict:
		if w.startswith(sub_s):
			cnt += 1
	# cnt > 0 means sub_s is a prefix of some words in the dictionary
	return cnt > 0


if __name__ == '__main__':
	main()
