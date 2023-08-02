"""
Searches for a list of vocabulary words in a named Anki deck.

Usage:
    search_deck.py
    search_deck.py --word-list-csv <word_list_file>
    search_deck.py --deck <deck_name> --kanji-field <kanji_field_name> --kana-field <kana_field_name>
"""


# std lib
import csv
import argparse
from typing import List, Tuple

# third party
import requests

# local
import lib


def load_words(file_path: str) -> List[Tuple[str, str]]:
    words = []

    with open(file_path, "r", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) != 2:
                print(f"WARNING: Unexpected row length {len(row)} for {row=}")
                continue
            words.append((row[0], row[1]))

    return words


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--word-list-csv", type=str, default="word_list.csv")
    parser.add_argument("--deck", type=str, default="Japanese Core 10K +Pics +Aud +Pitch")
    parser.add_argument("--kanji-field", type=str, default="vocab")
    parser.add_argument("--kana-field", type=str, default="vocab-kana")
    args = parser.parse_args()

    # Each word is (kanji, kana) tuple
    words: List[Tuple[str, str]] = load_words(args.word_list_csv)
