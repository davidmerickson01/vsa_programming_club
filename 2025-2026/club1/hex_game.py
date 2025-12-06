# from chatgpt

import random

def explain_hex_to_decimal(hex_str):
    explanation = []
    decimal_value = 0
    hex_digits = "0123456789ABCDEF"
    
    # Work through each digit from left to right
    for i, digit in enumerate(hex_str[::-1]):  # reverse for place value
        value = hex_digits.index(digit)
        place = 16 ** i
        contribution = value * place
        explanation.append(f"{digit} (={value}) × 16^{i} = {contribution}")
        decimal_value += contribution
    
    explanation_text = " + ".join(explanation[::-1]) + f" = {decimal_value}"
    return decimal_value, explanation_text

def hex_quiz():
    hex_digits = "0123456789ABCDEF"
    
    print("Welcome to the Hexadecimal Trainer!")
    print("Hexadecimal uses base 16 with digits 0-9 and A-F.")
    print("For example, A = 10, B = 11, ..., F = 15.\n")

    while True:
        # Generate a random 2-digit hex number
        hex_number = "".join(random.choice(hex_digits) for _ in range(random.randint(1,3)))
        print(f"What is hexadecimal {hex_number} in decimal?")

        try:
            user_answer = input("Your guess (or 'q' to quit): ").strip()
            if user_answer.lower() == 'q':
                print("Thanks for practicing! Goodbye!")
                break

            user_answer = int(user_answer)
            correct_answer, explanation = explain_hex_to_decimal(hex_number)

            if user_answer == correct_answer:
                print("✅ Correct! Nice job!")
            else:
                print(f"❌ Not quite. The correct answer is {correct_answer}.")

            print("Explanation:", explanation)
            print("-" * 50)

        except ValueError:
            print("Please enter a valid number or 'q' to quit.\n")

# Run the trainer
hex_quiz()

input("press ENTER to exit")
