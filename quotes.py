import json
import random

with open("quotes.json", encoding="utf-8") as f:
    quotes = json.load(f)["quotes"]

quote = random.choice(quotes)
print(quote["quote"] + " --" + quote["author"])


def read_quotes(filename):
    with open("quotes.json") as f:
        lines = (l.strip() for l in f)
        return [json.loads(l.decode("utf-8")) for l in lines if l]


def main():
    quotes = read_quotes("quotes.txt")
    authors = list(set(author for _, author in quotes))
    quote, _ = random.choice(quotes)
    author = random.choice(authors)
    print(quote.encode("utf-8"), "-", author.encode("utf-8"))


if __name__ == "__main__":
    main()
