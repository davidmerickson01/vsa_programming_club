# create a python program to play mastermind
# show me the code
# remove the try except code, and remove the command line parameters

#!/usr/bin/env python3
"""
Mastermind — simple terminal version (no try/except, no command-line arguments).
"""

import random
from collections import Counter

# Game settings
LENGTH = 4      # number of pegs
COLORS = 6      # colors represented as digits 1..COLORS
ATTEMPTS = 10   # number of tries allowed

def generate_code(length=LENGTH, colors=COLORS):
    """Return a list of random digits representing the secret code."""
    return [random.randint(1, colors) for _ in range(length)]

def parse_guess(text, length, colors):
    """Convert user input into a list of integers."""
    text = text.strip()
    if ' ' in text:
        parts = text.split()
    else:
        parts = list(text)
    if len(parts) != length:
        print(f"Guess must have {length} numbers.")
        return None
    guess = []
    for p in parts:
        if not p.isdigit():
            print("Each peg must be a number.")
            return None
        v = int(p)
        if not (1 <= v <= colors):
            print(f"Numbers must be between 1 and {colors}.")
            return None
        guess.append(v)
    return guess

def evaluate_guess(secret, guess):
    """Return (black, white) counts."""
    blacks = sum(1 for s, g in zip(secret, guess) if s == g)
    secret_count = Counter(secret)
    guess_count = Counter(guess)
    total_common = sum(min(secret_count[c], guess_count[c]) for c in secret_count)
    whites = total_common - blacks
    return blacks, whites

def pretty(code):
    """Return code as string."""
    return ' '.join(str(x) for x in code)

# Main game
print("Welcome to Mastermind!")
print(f"Guess the secret code of {LENGTH} digits (each 1–{COLORS}).")
print(f"You have {ATTEMPTS} attempts. Enter guesses like 1234 or 1 2 3 4.\n")

secret = generate_code(LENGTH, COLORS)
won = False

for attempt in range(1, ATTEMPTS + 1):
    guess = None
    while guess is None:
        raw = input(f"Attempt {attempt}/{ATTEMPTS} — your guess: ")
        guess = parse_guess(raw, LENGTH, COLORS)
    blacks, whites = evaluate_guess(secret, guess)
    if blacks == LENGTH:
        print(f"Congratulations! You cracked the code in {attempt} attempts: {pretty(secret)}")
        won = True
        break
    else:
        print(f"Result: {blacks} black, {whites} white\n")

if not won:
    print(f"Out of attempts! The secret code was: {pretty(secret)}")
