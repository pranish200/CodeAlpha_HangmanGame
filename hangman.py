import random

# Word list
word_list = ['python', 'code', 'alpha', 'intern', 'hangman']
chosen_word = random.choice(word_list)

# Game variables
guessed_letters = []
tries = 6

print("🎮 Welcome to Hangman!")

while tries > 0:
    display_word = ""
    for letter in chosen_word:
        if letter in guessed_letters:
            display_word += letter
        else:
            display_word += "_"

    print("Word:", display_word)
    
    if display_word == chosen_word:
        print("✅ Congratulations! You guessed the word correctly!")
        break

    guess = input("Guess a letter: ").lower()

    if guess in guessed_letters:
        print("⚠️ You already guessed that letter.")
        continue

    guessed_letters.append(guess)

    if guess not in chosen_word:
        tries -= 1
        print(f"❌ Wrong guess. Tries left: {tries}")

if tries == 0:
    print(f"😢 You lost! The word was: {chosen_word}")
