import json
import random
import uuid
import argparse


DIGITS = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"
}

NAMES = ["john", "emma", "sam", "rohit", "akshat", "michael", "sara"]
SURNAMES = ["doe", "lee", "kumar", "jain", "smith", "patel"]

CITIES = ["new york", "delhi", "mumbai", "paris", "berlin", "tokyo"]
LOCATIONS = ["airport", "hospital", "university", "mall"]

MONTHS = [
    "january", "feb", "march", "april", "may", "jun",
    "july", "august", "sept", "oct", "nov", "dec"
]


FILLERS = ["umm", "uhh", "ahh", "enna", "you know", "like"]

HOMOPHONES = {
    "for": "four",
    "to": "two",
    "too": "two",
    "won": "one",
    "ate": "eight"
}

def corrupt_word(word):
    """Apply random corruption to a word."""
    if random.random() < 0.1:
        return word.replace("o", "")       # drop o
    if random.random() < 0.1:
        return word.replace("e", "")       # drop e
    if random.random() < 0.1:
        return word[::-1]                  # reversed word
    if random.random() < 0.1:
        return word + random.choice(["a", "e", "i"])  # add vowel
    if random.random() < 0.1:
        return random.choice(FILLERS)
    return word


def corrupt_email_token(token):
    """Emails often get merged/mangled in STT."""
    if random.random() < 0.2:
        return token.replace(" ", "")               # remove spaces
    if random.random() < 0.1:
        return "".join(random.sample(token, len(token)))  # shuffle letters
    if random.random() < 0.2:
        return " ".join(list(token))                # spaced characters
    return token


def gen_credit_card():
    digits = "".join(str(random.randint(0, 9)) for _ in range(16))
    noisy = " ".join(DIGITS[d] for d in digits)

    parts = noisy.split()
    for i in range(len(parts)):
        if random.random() < 0.1:
            parts[i] = corrupt_word(parts[i])
    noisy = " ".join(parts)

    return noisy, digits


def gen_phone():
    digits = "".join(str(random.randint(0, 9)) for _ in range(10))
    parts = [DIGITS[d] for d in digits]

    if random.random() < 0.3:
        parts.insert(random.randint(0, 9), random.choice(FILLERS))
    if random.random() < 0.2:
        parts[random.randint(0, 9)] = corrupt_word(parts[random.randint(0, 9)])

    return " ".join(parts), digits


def gen_email():
    name = random.choice(NAMES)
    surname = random.choice(SURNAMES)
    domain = random.choice(["gmail", "yahoo", "outlook", "hotmail"])

    noisy = f"{name} dot {surname} at {domain} dot com"

    tokens = noisy.split()
    tokens = [corrupt_email_token(t) for t in tokens]
    noisy = " ".join(tokens)

    return noisy, f"{name}.{surname}@{domain}.com"


def gen_name():
    name = f"{random.choice(NAMES)} {random.choice(SURNAMES)}"
    tokens = name.split()
    tokens = [corrupt_word(t) for t in tokens]
    return " ".join(tokens), name


def gen_date():
    month = random.choice(MONTHS)
    day = random.randint(1, 28)
    year = random.randint(1990, 2024)
    noisy = f"{month} {day} {year}"

    # random swaps
    words = noisy.split()
    if random.random() < 0.1:
        random.shuffle(words)
        noisy = " ".join(words)

    return noisy, noisy


def gen_city():
    city = random.choice(CITIES)
    words = city.split()
    words = [corrupt_word(w) for w in words]
    return " ".join(words), city


def gen_location():
    loc = random.choice(LOCATIONS)
    return corrupt_word(loc), loc


TEMPLATES = {
    "CREDIT_CARD": gen_credit_card,
    "PHONE": gen_phone,
    "EMAIL": gen_email,
    "PERSON_NAME": gen_name,
    "DATE": gen_date,
    "CITY": gen_city,
    "LOCATION": gen_location,
}


def put_in_sentence(entity_text, label):
    """Embed entity inside a noisy STT-style sentence."""
    patterns = [
        f"my {label.lower().replace('_', ' ')} is {entity_text}",
        f"here is the {label.lower()} {entity_text}",
        f"{entity_text} is the {label.lower()}",
        f"you know the {label.lower()} {entity_text}",
        f"{entity_text} uh is my {label.lower()}",
    ]
    sent = random.choice(patterns).lower()

    for k, v in HOMOPHONES.items():
        if random.random() < 0.05:
            sent = sent.replace(k, v)

    sent = " ".join(sent.split())
    return sent



def build_example():
    label = random.choice(list(TEMPLATES.keys()))
    noisy_span, clean_span = TEMPLATES[label]()

    sentence = put_in_sentence(noisy_span, label)

    start = sentence.find(noisy_span)
    end = start + len(noisy_span)

    assert start != -1, "Span not found (debug needed)"

    return {
        "id": str(uuid.uuid4())[:8],
        "text": sentence,
        "entities": [
            {"start": start, "end": end, "label": label}
        ]
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="data/train_difficult.jsonl")
    ap.add_argument("--n", type=int, default=500)
    args = ap.parse_args()

    with open(args.output, "w") as f:
        for _ in range(args.n):
            ex = build_example()
            f.write(json.dumps(ex) + "\n")

    print(f"Generated {args.n} HARD STT augmented examples {args.output}")


if __name__ == "__main__":
    main()
