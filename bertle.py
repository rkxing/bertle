'''
BERTLE

Author: Robert Xing

-------------------

Inspired by The New York Times' web game Wordle, originally developed by Josh Wardle.

'''

import random
import string

TOTAL_GUESSES = 6
ALL_LETTERS_QWERTY = 'qwertyuiopasdfghjklzxcvbnm'
RULES = '''The rules are as follows:\n\n  1. Every game, the computer will choose a random existing English 5 letter word.
  2. The player has 6 attempts to guess the word.\n  3. After every guess, the results of that guess will be displayed as follows:
               -an \'X\' means that the letter guessed does not appear in the word.
               -an \'@\' means that the letter guessed does appear in the word, but it does not appear in the position it was guessed in.
               -a \'#\' means that the correct letter has been guessed in the correct position.
               -for players familiar with the game WORDLE, an \'X\' indicates a Gray letter, an \'@\' indicates a Yellow, and a \'#\' indicates a Green.
  4. The on-screen keyboard will also be updated after every guess such that "Gray" letters will be removed, while "Yellow" and "Green" letters will be capitalized.
  5. Only existing English 5 letter words are allowed as guesses.
  6. The game ends when either the word has been correctly guessed (All \'#\') or when the player has run out of guesses.'''
        

def load_lists():
    '''
    loads both lists for accepted guesses* and possible answers under original version of Wordle
    
    *the accepted guesses list has been modified to include the possible answers

    returns: pair consisting of (validGuesses:str list, validAnswers:str list)
    '''

    validGuessesFilename = "wordle-allowed-guesses.txt"
    validAnswersFilename = "wordle-answers-alphabetical.txt"

    inFileG = open(validGuessesFilename,'r')
    inFileA = open(validAnswersFilename,'r')

    validGuesses = [] #list of strings containing all accepted guesses + possible answers
    validAnswers = [] #list of strings containing all possible answers

    for line in inFileG:
        validGuesses.append(line.lower().strip())
    
    for line in inFileA:
        validAnswers.append(line.lower().strip())
    
    inFileG.close()
    inFileA.close()

    return (validGuesses,validAnswers)


def choose_word(validAnswers):
    '''
    chooses word to serve as the game solution

    takes: list of possible answers (validAnswers:str list)
    returns: randomly chosen word from the answer list (str)
    '''
    return random.choice(validAnswers)
    

def isValidGuess(guess, validGuesses):
    '''
    checks the guessed word against the list of valid guesses

    takes:
        - the user-guessed word (guess:str)
        - list of valid guesses/possible answers (validGuesses:str list)
    returns: bool
    '''
    return guess in validGuesses


def disp_guess_results(guess,answer):
    '''
    displays the results of every guess according to the following style:
        - if the guessed letter is not in the answer (Gray), display an 'X'
        - if in the answer but not in the right position (Yellow), display an '@'
        - if in the answer and in the right position (Green), display a '#'

    takes: 
        - the user-guessed word (guess:str)
        - computer-chosen answer (answer:str)
    returns: None
    '''

    results = [] #list to hold guess results

    guessL = list(guess) #lists to mutate in loop
    answerL = list(answer) 

    letters = list(answer) #list to keep track of already guessed letters

    for i in range(len(guessL)):
        if guessL[i] in answerL and guessL[i] in letters:

            dupTest = guess[guess.find(guessL[i]) + 1 : len(guess)] #slices guess to check for duplicate letters

            if guessL[i] == answerL[i]: #Green condition
                results.append('#')
                letters.remove(guessL[i])
            elif guessL[i] in dupTest: #duplicate letter condition
                results.append('X')
            else: #Yellow condition
                results.append('@') 
                letters.remove(guessL[i])

        else: #Gray condition
            results.append('X')

    print(''.join(results)) 


def disp_keyB(keyB):
    '''
    displays the on-screen keyboard in qwerty notation

    takes: the string containing the keyboard (keyB:str)
    returns: None
    '''

    ctr = 1 #counter for signalling line breaks

    for c in keyB:
        if ctr == 10: 
            print(c)
        elif ctr == 19:
            print(c)
            print(' ',end=' ')
        else: 
            print (c,end=' ')

        ctr += 1
        

def update_keyB(keyB,guess,answer):
    '''
    updates the on-screen keyboard based on guess:
        - Gray letters will be replaced with a space
        - Yellow/Green letters will become capitalized

    takes: 
        - currently available letters (keyB:str)
        - user-guessed word (guess:str) 
        - correct answer for the current game (answer:str)
    returns: updated string of keyB with proper modifications (str)
    '''

    newKeyb = list(keyB) #list to hold updated letters, later returned as a str

    for c in guess:
        if c in answer:
            if keyB.find(c.capitalize()) == -1: #checks if letter is already capitalized
                newKeyb[keyB.find(c)] = c.capitalize()
        else: #letter not in word aka Gray
            newKeyb[keyB.find(c)] = ' '

    return ''.join(newKeyb)


def play():
    '''
    main game function, starts a fresh game session with a new word each time it is called

    returns: None
    '''

    (validGuesses,validAnswers) = load_lists()
    answer = random.choice(validAnswers)
    guess = ''
    remainGuesses = TOTAL_GUESSES
    currentKeyb = ALL_LETTERS_QWERTY
    print()

    while (guess != answer and remainGuesses > 0):
        print('------------------------')

        disp_keyB(currentKeyb)
        print()
        print('Remaining guesses:',remainGuesses)
        guess = str(input('Enter a guess: ')).lower().strip()

        if not isValidGuess(guess,validGuesses):
            print('\n### Not in word list! ###')
            continue
        else: #valid guess
            print('               ',end='')
            disp_guess_results(guess,answer)
            currentKeyb = update_keyB(currentKeyb,guess,answer)
            remainGuesses -= 1

    print('------------------------')

    if guess == answer:
        print('Solved!')
        print('You solved this BERTLE in',TOTAL_GUESSES-remainGuesses,'guesses.')
    else: #broke out of loop with remainGuess == 0
        print('No guesses remaining.')
        print('The correct answer was \''+answer+'\'')


def main():
    '''
    main function that starts program and runs menu

    returns: None
    '''

    print('Welcome to BERTLE\n')

    while(True):
        print('------------------------')
        print('1. Play Game')
        print('2. Read Rules')
        print('3. Exit\n')
        choice = int(input('Please enter a selection: '))

        if choice == 1:
            play()
        elif choice == 2:
            print('\n------------------------\n')
            print(RULES+'\n')
        elif choice == 3:
            exit()
        else:
            print('### Invalid selection ###')


#driver code
if __name__ == '__main__':
    main()