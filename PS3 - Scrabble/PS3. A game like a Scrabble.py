
"""
This game is a lot like Scrabble or Words With 
Friends. Letters are dealt to players, who then construct one or more words
using their letters. Each ​valid​ word earns the user points, based on the
length of the word and the letters in that word. 

"""


import math
import random


VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
SCRABBLE_LETTER_VALUES = {
    '*':0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2,
    'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1,
    'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4,
    'x': 8, 'y': 4, 'z': 10
}


WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    infile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in infile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq

	
#
# Problem #1: Scoring a word
#


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    score1 = 0
    if word == '':
        return 0
    word = word.lower()
    for i in word:
        score1 += SCRABBLE_LETTER_VALUES.get(i)
    score0 = 7*len(word) - 3*(n-len(word))
    score2 = max(1, score0)
    score = score1*score2
    return score

    
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')    # print all on the same line
    print()                              # print an empty line


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand = {}
    num_vowels = int(math.ceil(n/3))-1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    hand['*'] = 1
    
    return hand


#
# Problem #2: Update a hand by removing letters
#


def update_hand(hand, word):
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    word = word.lower()
    new_hand = hand.copy()
    for letter in word:
        if letter in new_hand:
            if new_hand[letter] > 1:
                new_hand[letter] -= 1
            else:
                del (new_hand[letter])
    return new_hand


#
# Problem #3: Test word validity
#


def is_valid_word_support(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    new_hand = hand.copy()
    for i in word:
        if i not in new_hand:
            return False
        new_hand = update_hand(new_hand, i)
    return word in word_list


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is valid. Otherwise, returns False.
    Does not mutate hand or word_list.
    """
    word = word.lower()
    if not '*' in word:
        return is_valid_word_support(word, hand, word_list)
    else:
        for i in range(len(word)):
            if word[i] == '*':
                for j in 'aoiue':
                    word = word[0:i] + j + word[i+1:len(word)]
                    temp_hand = hand.copy()
                    if j in hand:
                        temp_hand[j] += 1
                    else:
                        temp_hand[j] = 1
                    if is_valid_word_support(word, temp_hand, word_list) == True:
                        return True
    return False


#
# Problem #5: Playing a hand
#


def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """

    handlen = 0
    for letter in hand.keys():
        for j in range(hand[letter]):
            handlen += 1
    return handlen

                   
def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    earned_points = 0
    earned = 0
    while hand != {}:
        print('​Current hand:', end=' ')
        display_hand(hand)
        word = input("Enter word, or '!!' to indicate that you are finished: ")
        if word == '!!':
            print('Ran out of letters. Total score of this hand:', \
                  earned_points, 'point\'s')
            print('__________________________________')
            print(' ')
            break
        if is_valid_word(word, hand, word_list):
            earned = get_word_score(word, calculate_handlen(hand))
            earned_points += earned
            print('\"'+word+'\"', 'earned', earned, 'points. Total: ', \
                  earned_points, 'point\'s')
        else:
            print('That is not a valid word. Please choose another word .')
        hand = update_hand(hand, word)
        print(' ')
    if word != '!!':
        print('Ran out of letters. Total score of this hand:', earned_points, \
              'point\'s')
        print('__________________________________')
        print(' ')
    return earned_points


#
# Problem #6: Playing a game
# 


def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by
    user)with a new letter chosen from the VOWELS and CONSONANTS at random. The
    new letter should be different from user's choice, and should not be any of
    the letters already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    letter = letter.lower()
    if letter not in hand:
        print (' ')
        return hand
    new_hand = hand.copy()
    available_letters = ''
    letters = VOWELS + CONSONANTS
    for i in letters:
        if i not in new_hand.keys():
            available_letters += i
    del(new_hand[letter])
    new_hand[random.choice(available_letters)] = hand[letter]
    return new_hand
    
    
def play_game(word_list):

    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

    * Note: if you replay a hand, you do not get the option to substitute
      a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    while True:
        try:
            number_of_hands = int(input('Enter total number of hands: '))
        except:
            print ('Enter decimal number!')
            print('')
        else:
            break
        
    total_earned = 0
    replays_left = 1
    for i in range(number_of_hands):
        n = 10
        hand = deal_hand(n)
        print ('Current hand:', end=' ')
        display_hand(hand)
        substitute = input ('Would you like to substitute a letter? ')
        if substitute.lower() == 'yes':
            letter = input('Which letter would you like to replace: ')
            hand = substitute_hand(hand, letter)
        print (' ')
        saved_hand = hand.copy()
        earned_points = play_hand(hand, word_list)
        if replays_left == 1:
            replay = input('Would you like to replay the hand? ')
            if replay.lower() == 'yes':
                replays_left -= 1
                hand = saved_hand
                print ('Current hand:', end=' ')
                earned_points_replayed = play_hand(hand, word_list)
                earned_points = max(earned_points_replayed, earned_points)    
        total_earned += earned_points
    print ('Total score over all hands:', total_earned, 'point\'s')
        

if __name__ == '__main__':
    WORD_LIST = load_words()
    play_game(WORD_LIST)
