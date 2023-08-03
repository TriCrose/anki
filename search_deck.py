"""
Searches for a list of vocabulary words in a named Anki deck and reports missing ones.

Usage:
    search_deck.py
    search_deck.py --word-list-csv <word_list_file>
    search_deck.py --deck <deck_name> --kanji-field <kanji_field_name> --kana-field <kana_field_name>
"""


# std lib
import os
import csv
import json
import argparse
from typing import List, Set, Dict, Tuple, Any

# third party
import requests

# local
import lib


def is_katakana(text: str) -> bool:
    # TODO
    return False


def load_words(file_path: str) -> Set[Tuple[str, str]]:
    words = set()

    with open(file_path, "r", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) != 2:
                print(f"WARNING: Unexpected row length {len(row)} for {row=}")
                continue
            words.add((row[0], row[1]))

    return words


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--word-list-csv", type=str, default="word_list.csv")
    parser.add_argument("--deck", type=str, default="Japanese Core 10K +Pics +Aud +Pitch")
    parser.add_argument("--kanji-field", type=str, default="vocab")
    parser.add_argument("--kana-field", type=str, default="vocab-kana")
    parser.add_argument("--output", type=str, default="missing_words.csv")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    assert not os.path.exists(args.output), f"Output file '{args.output}' already exists"

    # Check the deck exists
    decks = lib.anki("deckNames")
    assert args.deck in decks, f"Deck '{args.deck}' not found in Anki ({decks=})"

    # Get all the notes
    note_ids: List[int] = lib.anki("findNotes", query=f'"deck:{args.deck}"')
    notes: List[Dict[str, Any]] = lib.anki("notesInfo", notes=note_ids)

    # Fetch all the kanji/kana from the notes
    words = set()
    for note in notes:
        note_id = note["noteId"]
        fields = note["fields"]
        if args.kanji_field not in fields or args.kana_field not in fields:
            if args.verbose:
                pretty_note = json.dumps(note, indent=4)
                print(f"Note {note_id} is missing kana and/or kanji fields:\n{pretty_note}\n")
            else:
                print(f"Note {note_id} is missing kana and/or kanji fields")
            continue

        kanji = fields[args.kanji_field]["value"]
        kana = fields[args.kana_field]["value"]

        if is_katakana(kanji):
            kana = kanji

        if kanji == kana:
            kanji = ""

        words.add((kanji, kana))

    # Find which ones are missing
    missing_words = load_words(args.word_list_csv).difference(words)
    print(f"{len(missing_words)} words are missing from deck '{args.deck}'")

    with open(args.output, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        for word in missing_words:
            writer.writerow([word[0], word[1]])
    print(f"Words written to {args.output}")

    if args.verbose:
        print(f"{missing_words=}")
