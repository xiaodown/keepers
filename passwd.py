#!/usr/bin/env python3

import secrets
import string

def main():
    upperbool = ask_yes_no("Use uppercase letters?")
    lowerbool = ask_yes_no("Use lowercase letters?")
    punctbool = ask_yes_no("Use punctuation?")
    pwlength = int(input("Enter password length: "))

    newpw = generate_random_string(pwlength, upperbool, lowerbool, punctbool)
    print(f"Your new password is: {newpw}")

def safe_punctuation():
    # Exclude backtick, single quote, double quote, backslash, semicolon
    unsafe_chars = '`\'"\\;'
    return ''.join(ch for ch in string.punctuation if ch not in unsafe_chars)

def generate_random_string(length, upper=False, lower=False, punct=False):
    alphabet = ''
    if upper:
        alphabet += string.ascii_uppercase
    if lower:
        alphabet += string.ascii_lowercase
    if punct:
        alphabet += safe_punctuation()
    
    return ''.join(secrets.choice(alphabet) for i in range(length))

def ask_yes_no(question):
    while True:
        response = input(question + ' (y/n): ').lower()
        if response in ['y', 'n']:
            return response == 'y'
        else:
            print("Please enter y or n.")

main()

