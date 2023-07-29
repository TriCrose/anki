"""
Main index: https://www.kanshudo.com/collections/vocab_usefulness2021
* Each group (usefulness level) is a div.infopanel (assert that there are 5)
* Within the div.infopanel there is a "div.coll2 spaced", within which there is a div.coll2_div
* Within that div, there is an <a> tag which links to one of the sets of 100 (assert the innerHTML of the <a> is as expected)

For each page:
* Each entry is contained within a `div.jukugorow first last`
* Within that there is a div.furigana whose innerHTML contains the furigana
* Then there is also a div.f_kanji whose innerHTML contains the kanji
"""


import os
import csv
import time
import http

import bs4
import requests

from typing import List, Tuple


BASE_URL = "https://www.kanshudo.com"
INDEX_PAGE_URL = f"{BASE_URL}/collections/vocab_usefulness2021"


def get_soup(url: str) -> bs4.BeautifulSoup:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    print(f"Fetching page {url} with {headers=}")

    res = requests.get(url, headers=headers)
    assert (
        res.status_code == http.HTTPStatus.OK
    ), f"Server returned {res.status_code} {res.reason}"

    return bs4.BeautifulSoup(res.content, "html.parser")


def download_all_kanji(urls: List[Tuple[str, int]], output_file: str, page_delay=500) -> None:
    assert not os.path.exists(output_file), f"Output file '{output_file}' already exists"

    with open(output_file, "w") as f:
        writer = csv.writer(f)

        for url, count in urls:
            soup = get_soup(url)
            kanji_entries = soup.find_all("div", class_="jukugorow first last")
            if len(kanji_entries) != count:
                print(f"WARNING: Expected {count} kanji entries, found {len(kanji_entries)}")

            for entry in kanji_entries:
                found_kanji = False
                kanji: List[str] = []
                kana: List[str] = []

                for child in entry.find("a").children:
                    if isinstance(child, bs4.element.NavigableString):
                        kanji.append(child)
                        kana.append(child)
                    elif child.name == "span":
                        found_kanji = True
                        kanji.append(child.find("div", class_="f_kanji").decode_contents())
                        kana.append(child.find("div", class_="furigana").decode_contents())
                    else:
                        print(f"WARNING: Unexpected a child of <a> tag: {child=}")

                if not found_kanji:
                    kanji = []
                writer.writerow(["".join(kanji), "".join(kana)])

            time.sleep(page_delay / 1000.0)


if __name__ == "__main__":
    info_panels = get_soup(INDEX_PAGE_URL).find_all("div", class_="infopanel")
    assert (
        len(info_panels) == 5
    ), f"Expected 5 'div.infopanel's, but got {len(info_panels)}"

    urls_with_counts: List[Tuple[str, int]] = []

    for i, panel in enumerate(info_panels):
        table = panel.find("div", class_="coll2 spaced")
        prev_upper_bound = 0
        print(f"\nGroup {i+1}")

        for j, div in enumerate(table.find_all("div")):
            a_tag = div.find("a")

            word_range = a_tag.decode_contents()
            lower_bound = int(word_range.split("-")[0])
            upper_bound = int(word_range.split("-")[1])

            assert (
                lower_bound == 1 or lower_bound == prev_upper_bound + 1
            ), f"Word ranges are not continuous (went from {prev_upper_bound} to {lower_bound})"
            prev_upper_bound = upper_bound

            link = BASE_URL + a_tag["href"]
            urls_with_counts.append((link, upper_bound - lower_bound + 1))
            print(f"{word_range:>10}: {link}")

    download_all_kanji(urls_with_counts, "output.csv")
