import requests
from bs4 import BeautifulSoup
from db import session
from models import Tag, Author, Quote


def parse_date(url_, parse_page_):
    data = []
    for num_page in range(1, parse_page_):
        response = requests.get(f"{url_}/page/{num_page}/")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            quotes = soup.find_all('span', class_='text')
            authors = soup.find_all('small', class_='author')
            tags = soup.find_all('div', class_='tags')
            authors_href = soup.find_all('div', class_='quote')
            for i in range(0, len(quotes)):
                quote = quotes[i].text.replace("“", "").replace("”", "").replace("\r", "").replace("\n", "")
                author = authors[i].text
                list_tag = []
                tags_for_quotes = tags[i].find_all('a', class_='tag')
                for tags_for_quote in tags_for_quotes:
                    list_tag.append(tags_for_quote.text)
                for a in authors_href[i].find_all('a'):
                    if a.text == '(about)':
                        href = f"{url_}{a['href']}"
                        data.append({"quote": quote,
                                     "author": author,
                                     "tag": list_tag,
                                     "href": href})
    return data


def is_quote_db(quote_):
    quote_db = session.query(Quote).filter_by(name=quote_).first()
    return True if quote_db else False


def add_data_db(el_):
    if not is_quote_db(el_.get('quote')):
        author_from_db = session.query(Author).filter_by(name=el_.get('author')).first()
        if author_from_db:
            author_id = author_from_db.id
        else:
            author = Author(name=el_.get('author'), href_author=el_.get('href'))
            session.add(author)
            session.commit()
            author_id = author.id
        quote = Quote(name=el_.get('quote'), author_id=author_id)
        session.add(quote)
        session.commit()
        tag_for_quote = []
        for el_tag in el_.get('tag'):
            tag_from_db = session.query(Tag).filter_by(name=el_tag).first()
            if tag_from_db:
                tag_for_quote.append(tag_from_db)
            else:
                tag = Tag(name=el_tag)
                tag_for_quote.append(tag)
                session.add(tag)
        quote.tags = tag_for_quote
        session.commit()


def quotes_by_tag(tag_):
    quotes = session.query(Quote).join(Quote.tags).filter(Tag.name == tag_).all()
    return quotes


if __name__ == '__main__':
    url = 'https://quotes.toscrape.com'
    parse_page = 5

    store = parse_date(url, parse_page)
    for el in store:
        add_data_db(el)
    for q in quotes_by_tag('life'):
        print(q.name)
    session.close()
