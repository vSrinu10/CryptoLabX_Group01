from collections import Counter

def analyze_file(path):
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    print("\nFile Analysis")
    print("----------------------")
    print("Characters :", len(text))
    print("Words :", len(text.split()))
    print("Lines :", len(text.splitlines()))
    print("Unique Characters :", len(set(text)))

    letters = [c.lower() for c in text if c.isalpha()]
    freq = Counter(letters)

    print("\nLetter Frequency")
    for letter in sorted(freq):
        print(letter, ":", freq[letter])
