import re

DIGIT_MAP = {
    "zero": "0", "oh": "0",
    "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
}

def normalize_digits(text):
    parts = text.lower().split()
    digits = [DIGIT_MAP.get(p, "") for p in parts]
    return "".join(digits)


def valid_email(text):
    t = text.lower().replace(" dot ", ".").replace(" at ", "@")
    return re.match(r"^[a-z0-9_.]+@[a-z0-9_.]+$", t) is not None


def valid_phone(text):
    nums = normalize_digits(text)
    return len(nums) >= 7 and nums.isdigit()


def valid_credit_card(text):
    nums = normalize_digits(text)
    return len(nums) >= 13 and len(nums) <= 19 and nums.isdigit()


def valid_person(text):
    if len(text) < 2: 
        return False
    if text.isdigit():
        return False
    return True


def validate_span(label, text):
    if label == "EMAIL":
        return valid_email(text)
    if label == "PHONE":
        return valid_phone(text)
    if label == "CREDIT_CARD":
        return valid_credit_card(text)
    if label == "PERSON_NAME":
        return valid_person(text)
    if label == "DATE":
        return True
    return True
