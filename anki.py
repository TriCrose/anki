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


import time
import http

import bs4
import requests

from typing import List


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


def download_all_kanji(urls: List[str], page_delay=500) -> None:
    for url in urls:
        soup = get_soup(url)
        time.sleep(page_delay / 1000.0)


if __name__ == "__main__":
    info_panels = get_soup(INDEX_PAGE_URL).find_all("div", class_="infopanel")
    assert (
        len(info_panels) == 5
    ), f"Expected 5 'div.infopanel's, but got {len(info_panels)}"

    urls = []

    for i, panel in enumerate(info_panels):
        table = panel.find("div", class_="coll2 spaced")
        prev_upper_bound = 0
        print(f"\nGroup {i+1}")

        for j, div in enumerate(table.find_all("div")):
            a_tag = div.find("a")
            link = BASE_URL + a_tag["href"]
            urls.append(link)

            word_range = a_tag.decode_contents()
            lower_bound = int(word_range.split("-")[0])
            upper_bound = int(word_range.split("-")[1])

            assert (
                lower_bound == 1 or lower_bound == prev_upper_bound + 1
            ), f"Word ranges are not continuous (went from {prev_upper_bound} to {lower_bound})"

            prev_upper_bound = upper_bound
            print(f"{word_range:>10}: {link}")

    download_all_kanji(urls)
