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

import bs4
import http
import requests
from typing import List

BASE_URL = "https://www.kanshudo.com"
INDEX_PAGE_URL = f"{BASE_URL}/collections/vocab_usefulness2021"
USER_AGENT_STR = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

def download_all_kanji(urls: List[str]) -> None:
    pass

if __name__ == "__main__":
    # Get HTML
    res = requests.get(INDEX_PAGE_URL, headers={"User-Agent": USER_AGENT_STR})
    assert res.status_code == http.HTTPStatus.OK, f"Status code is {res.status_code}"

    # Parse it
    soup = bs4.BeautifulSoup(res.content, "html.parser")

    # There should be five usefulness levels, organised into "info panels"
    info_panels = soup.find_all("div", class_="infopanel")
    assert len(info_panels) == 5, f"Expected 5 'div.infopanel's, but got {len(info_panels)}"

    urls = []

    for i, panel in enumerate(info_panels):
        table = panel.find("div", class_="coll2 spaced")

        for j, div in enumerate(table.find_all("div")):
            a_tag = div.find("a")
            link = BASE_URL + a_tag["href"]
            urls.append(link)

            # Print the links to the console
            word_range = a_tag.decode_contents()
            print(f"{word_range:>10}: {link}")

    download_all_kanji(urls)
