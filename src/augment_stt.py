import json
import random
import uuid
import argparse


DIGITS = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"
}

FILLER_WORDS = ["uh", "um", "you know", "like"]

NAMES = [
    "john doe", "amy lee", "michael smith", "sara johnson",
    "rohit kumar", "akshat jain", "emma davis"
]

CITIES = ["new york", "san francisco", "mumbai", "delhi", "paris", "berlin"]
LOCATIONS = ["airport", "railway station", "university", "hospital"]

MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]


def random_cc():
    digits = "".join(str(random.randint(0, 9)) for _ in range(16))
    # spell out digits
    return " ".join(DIGITS[d] for d in digits), digits


def random_phone():
    digits = "".join(str(random.randint(0, 9)) for _ in range(10))
    return " ".join(DIGITS[d] for d in digits), digits


def random_email():
    username = random.choice(["john", "amy", "test", "admin", "user"])
    domain = random.choice(["gmail", "yahoo", "hotmail"])
    email = f"{username}.{domain}@example.com"
    noisy = email.replace(".", " dot ").replace("@", " at ")
    return noisy, email


def random_date():
    day = random.randint(1, 28)
    month = random.choice(MONTHS)
    year = random.randint(1990, 2024)
    return f"{month} {day} {year}"


def maybe_filler(text):
    if random.random() < 0.3:
        fw = random.choice(FILLER_WORDS)
        return f"{fw} {text}"
    return text


def generate_example():
    template_type = random.choice([
        "credit_card", "phone", "email", "name", "date",
        "city", "location"
    ])

    if template_type == "credit_card":
        noisy, raw = random_cc()
        base = f"my credit card number is {noisy}"
        label = "CREDIT_CARD"
        span_text = noisy

    elif template_type == "phone":
        noisy, raw = random_phone()
        base = f"my phone number is {noisy}"
        label = "PHONE"
        span_text = noisy

    elif template_type == "email":
        noisy, raw = random_email()
        base = f"my email is {noisy}"
        label = "EMAIL"
        span_text = noisy

    elif template_type == "name":
        name = random.choice(NAMES)
        base = f"my name is {name}"
        label = "PERSON_NAME"
        span_text = name

    elif template_type == "date":
        dt = random_date()
        base = f"i met him on {dt}"
        label = "DATE"
        span_text = dt

    elif template_type == "city":
        city = random.choice(CITIES)
        base = f"i live in {city}"
        label = "CITY"
        span_text = city

    else:
        loc = random.choice(LOCATIONS)
        base = f"he went to the {loc}"
        label = "LOCATION"
        span_text = loc

    sentence = maybe_filler(base).lower()

    sentence = " ".join(sentence.split())

    start = sentence.find(span_text)
    end = start + len(span_text)

    assert start != -1, "Span not found - debugging required"

    return {
        "id": str(uuid.uuid4())[:8],
        "text": sentence,
        "entities": [
            {"start": start, "end": end, "label": label}
        ]
    }




def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="data/augmented.jsonl")
    ap.add_argument("--n", type=int, default=500)
    args = ap.parse_args()

    with open(args.output, "w", encoding="utf-8") as f:
        for _ in range(args.n):
            ex = generate_example()
            f.write(json.dumps(ex) + "\n")

    print(f"✓ Generated {args.n} noisy STT examples → {args.output}")


if __name__ == "__main__":
    main()
