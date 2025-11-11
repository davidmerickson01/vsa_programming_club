# https://copilot.microsoft.com/
# write python program that is a guessing game for the capitals of europe

import random

# Dictionary of European countries and their capitals
european_capitals = {
    "France": "Paris",
    "Germany": "Berlin",
    "Italy": "Rome",
    "Spain": "Madrid",
    "Portugal": "Lisbon",
    "Netherlands": "Amsterdam",
    "Belgium": "Brussels",
    "Sweden": "Stockholm",
    "Norway": "Oslo",
    "Denmark": "Copenhagen",
    "Finland": "Helsinki",
    "Poland": "Warsaw",
    "Austria": "Vienna",
    "Switzerland": "Bern",
    "Greece": "Athens",
    "Czech Republic": "Prague",
    "Hungary": "Budapest",
    "Ireland": "Dublin",
    "Croatia": "Zagreb",
    "Slovakia": "Bratislava",
    "Slovenia": "Ljubljana",
    "Romania": "Bucharest",
    "Bulgaria": "Sofia",
    "Serbia": "Belgrade",
    "Ukraine": "Kyiv"
}

def play_game():
    score = 0
    countries = list(european_capitals.keys())
    random.shuffle(countries)

    print("Welcome to the European Capitals Guessing Game!")
    print("Type 'exit' to quit at any time.\n")

    for country in countries:
        answer = input(f"What is the capital of {country}? ").strip()
        if answer.lower() == 'exit':
            break
        elif answer.lower() == european_capitals[country].lower():
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The capital of {country} is {european_capitals[country]}.\n")

    print(f"Game over! Your final score is {score}/{len(countries)}.")

if __name__ == "__main__":
    play_game()
