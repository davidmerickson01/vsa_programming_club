import random

print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")
print("You have 10 tries to guess it correctly.")

secret_number = random.randint(1, 100)

for attempts in range(1, 11):
    guess_input = input(f"Attempt {attempts}: Enter your guess: ")

    if not guess_input.isdigit():
        print("Please enter a valid number.")
        continue

    guess = int(guess_input)

    if guess < 1 or guess > 100:
        print("Please guess a number between 1 and 100.")
        continue

    if guess < secret_number:
        print("Too low! Try again.")
    elif guess > secret_number:
        print("Too high! Try again.")
    else:
        print(f"🎉 Congratulations! You guessed it in {attempts} tries.")
        break
else:
    # This runs if the loop completes without a break
    print(f"😢 Sorry, you're out of tries! The number was {secret_number}.")

input("Press ENTER to exit")
