from db_mongo import url
from mongoengine import connect

from models import Authors, Quotes
########################
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes.settings')
import django
from django.conf import settings

if not settings.configured:
    django.setup()

#############################################
from app_quotes.models import Quote, Tag, Author

con = connect(host=url, ssl=True)


def migrate_author(author_obj):
    if not Author.objects.filter(fullname=author_obj.fullname):
        author = Author(fullname=author_obj.fullname)
        author.save()
        print(f"Author name: {author_obj.fullname} add to db_postgres.")


def migrate_tag(quote_obj):
    for tag in quote_obj.tags:
        if not Tag.objects.filter(tag=tag):
            new_tag = Tag(tag=tag)
            new_tag.save()
            print(f"Tag: {tag} added to db_postgres.")


def main():
    authors = Authors.objects()
    quotes = Quotes.objects()

    for author in authors:
        migrate_author(author)

    for quote in quotes:
        migrate_tag(quote)

        new_quote = Quote(description=quote.quote,
                          author=Author.objects.get(fullname=quote.author.fullname))
        print(f"Quote added: {new_quote.description}\nAuthor: {new_quote.author}")
        new_quote.save()
        for tag in quote.tags:
            new_quote.tag.add(Tag.objects.get(tag=tag))
        new_quote.save()

    con.close()


if __name__ == "__main__":
    main()
