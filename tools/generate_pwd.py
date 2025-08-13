import random
import string

def generate_password(length: int):
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    symbols = string.punctuation

    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols)
    ]

    all_chars = lowercase + uppercase + digits + symbols
    password += random.choices(all_chars, k=length - 4)

    return ''.join(password)
