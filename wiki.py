"""
# @ author: Takfarinas Saber
# @ about: this code searches information on Wikipedia about a given term and prints the result
# @ usage: python3 wiki.py "Barack Obama"
#       e.g.  python3 wiki.py "Barack Obama"
"""

# ====================================================================================== #
# This script (wiki.py) is NOT run on the host machine
# I have just included it in this repository in case it is needed for grading purposes
# ====================================================================================== #

import wikipedia
import sys


def search_wikipedia(term):
    page_ids = wikipedia.search(term)
    pages = []

    for page_id in page_ids:
        try:
            page = wikipedia.page(page_id)
            pages.append(page)
        except:
            pass
    if len(pages) >= 0:
        for page in pages:
            print(f"\nTitle: {page.title}")
            print(f"\nURL: {page.url}")
            print(f"\nContent: {page.content}\n")
    else:
        return "No Results!"


arguments = "".join(sys.argv[1:])
search_wikipedia(arguments)