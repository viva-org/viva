import PyPDF2
import re
import os
from collections import Counter
from typing import List, Set

from infrastructure.database.brick_repository import BrickRepository

def extract_words_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.pdf':
        return extract_words_from_pdf(file_path)
    elif file_extension.lower() == '.txt':
        return extract_words_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

def extract_words_from_pdf(pdf_path):
    words = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            words.extend(extract_words_from_text(text))
    return words

def extract_words_from_txt(txt_path):
    words = []
    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            words.extend(extract_words_from_text(line))
    return words

def extract_words_from_text(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def count_words(words):
    return Counter(words)

def compare_words(pdf_words: Counter, brick_words: Set[str]):
    new_words = []
    for word, count in pdf_words.most_common():
        # 只保留大于 2 次的单词
        if word not in brick_words and count > 2:
            new_words.append((word, count))
    return new_words

def save_new_words(new_words, output_file):
    with open(output_file, 'w') as file:
        for word, count in new_words:
            file.write(f"{word}: {count}\n")

def main():
    file_path = "[English (auto-generated)] Google x-CEO Eric Schmidt's BANNED Stanford talk_ They Don't Want You to Know This About Remote Work [DownSub.com].txt"
    output_file = "new_words.txt"
    words = extract_words_from_file(file_path)
    word_counts = count_words(words)
    bricks = BrickRepository('postgresql://root:root@localhost/root').get_all_bricks()
    brick_words = set(brick.spelling.lower() for brick in bricks if brick.spelling)
    new_words = compare_words(word_counts, brick_words)
    save_new_words(new_words, output_file)
    print(f"New words and their counts have been saved to {output_file}")

if __name__ == "__main__":
    bricks = BrickRepository('postgresql://root:root@localhost/root').get_all_bricks()
    print(bricks[5])