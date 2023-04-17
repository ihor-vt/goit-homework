from pathlib import Path
from json import load

from models import Authors, Quotes

"""
Create authors and quotes in json files.
"""

PATH_AUTHORS = Path("./authors.json")
PATH_QUOTES = Path("/.quotes.json")


def create_authors(json_authors, json_quotes):
    for author in json_authors:
        db_author = Authors(
                fullname=author["fullname"],
                born_date=author["born_date"],
                born_location=author["born_location"],
                description=author["description"],
                ).save()
        
        create_quoters(json_quotes, db_author)


def create_quoters(quoters, author):
    for quotes in quoters:
        if quotes['author'] == author.fullname:
            db_quote = Quotes(
                tags=quotes["tags"],
                author=author,
                quote=quotes["quote"]
            ).save()


def main():
    with open(PATH_AUTHORS) as file:
        authors = load(file)

    with open(PATH_QUOTES) as file:
        quoters = load(file)

    create_authors(authors, quoters)


if __name__ == '__main__':
    main()