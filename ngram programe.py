import random
from collections import defaultdict, Counter
import re

class NGramTextGenerator:
    def __init__(self, n):
        self.n = n
        self.ngrams = defaultdict(Counter)

    def read_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        words = self.tokenize(text)
        return words

    def tokenize(self, text):
        words = re.findall(r'\b\w+\b', text)
        return words

    def generate_ngram_model(self, words):
        for word in words:
            characters = list(word) + [None]
            for i in range(len(characters) - self.n):
                gram = tuple(characters[i:i + self.n])
                next_char = characters[i + self.n]
                self.ngrams[gram][next_char] += 1

        ngram_probabilities = {}
        for gram, counter in self.ngrams.items():
            total_count = sum(counter.values())
            probabilities = {}
            for char, count in counter.items():
                rate = count / total_count
                probabilities[char] = rate
            ngram_probabilities[gram] = probabilities
        self.ngrams = ngram_probabilities

    def generate_next_char(self, seed):
        current = tuple(seed)
        if current in self.ngrams:
            probabilities = self.ngrams[current]
            next_char = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]
            return next_char
        else:
            return None

    def generate_text(self, seed):
        result = list(seed)
        while True:
            next_char = self.generate_next_char(result[-self.n:])
            if next_char is None:
                break
            result.append(next_char)
        return ''.join(filter(None, result))

def main():
    n = int(input("Enter the length of n-gram: "))
    filename = r"C:\Users\dmmao\Desktop\5100 AI\HW1\transcript.txt"

    generator = NGramTextGenerator(n)
    words = generator.read_file(filename)
    generator.generate_ngram_model(words)

    seed = input(f"Enter {n} characters to start the generation: ")
    if len(seed) < n:
        print("Seed text is too short.")
        return

    generated_text = generator.generate_text(seed)
    print(f"Generated text: {generated_text}")

if __name__ == "__main__":
    main()