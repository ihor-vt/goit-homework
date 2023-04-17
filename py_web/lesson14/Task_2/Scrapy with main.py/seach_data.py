import redis
from redis_lru import RedisLRU
from sys import exit

from models import Authors, Quotes

"""
Search script in a cloud database Atlas MongoDB.
start -> in terminal: py search_script.py
reid_lru caching is implemented
commands: 
    name: Steve Martin — знайти та повернути список всіх цитат автора Steve Martin;
    tag:life — знайти та повернути список цитат для тега life;
    tags:life,live — знайти та повернути список цитат, де є теги life або live (примітка: без пробілів між тегами life, live);
    exit — завершити виконання скрипту;
"""

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@cache
def name(author_name: str) -> str:
    """
    name: Steve Martin — знайти та повернути список всіх цитат автора Steve Martin.
    :param user_name:
    :return:
    """
    authors = Authors.objects()

    for author in authors:
            if author.fullname in author_name:
                quotes = Quotes.objects()

                for quote in quotes:
                    if author.id.__str__() in quote.author.id.__str__():
                        return quote.quote
    return f"No matches."

@cache
def tag(user_tag: str) -> list | str:
    """
    tag:life — знайти та повернути список цитат для тега life;
    :param user_tag:
    :return:
    """
    result = []

    quotes = Quotes.objects()

    for quote in quotes:
        for value in quote.tags:
            if value in user_tag:
                result.append(quote.quote)

    if len(result) == 0:
        return f"No matches."

    return result


@cache
def tags(user_tags: str):
    """
    tags:life,live — знайти та повернути список цитат, де є теги life або live (примітка: без пробілів між тегами life, live);
    :param user_tags:
    :return:
    """
    tags_ = user_tags.split(",")
    result = set()

    for tag_ in tags_:
        tags_ = tag(tag_)
        if "No matches." in tags_:
            continue
        for value in tags_:
            result.add(value)

    return list(result)


@cache
def filter_data_tag(seach, document):
    result = []
    for tag in document.filter(tags__contains=seach):
        result.append(tag.quote)

    if len(result) == 0:
        return f"No matches."
    
    return result


@cache
def filter_data_name(seach, document):
    result = []
    for author in document.filter(fullname__contains=seach):
        quotes = Quotes.objects()
        for quote in quotes:
            if author.id.__str__() in quote.author.id.__str__():
                result.append(quote.quote)

    if len(result) == 0:
        return f"No matches."
    
    return result


@cache
def seach_regex(user_input: str):
    """
    name:Steve Martin та tag:life можливість скороченого запису значень для пошуку, як name:st та tag:li відповідно
    """
    if 'tag' in user_input:
        quotes = Quotes.objects
        seach = user_input.split('tag: ')[0]
        result = filter_data_tag(seach, quotes)
    elif 'name' in user_input:
        authors = Authors.objects
        seach = user_input.split('name: ')[0]
        result = filter_data_name(seach, authors)

    return result


def exits():
    exit()


def hadlde_command(user_input: str):
    command = {
        "name": name,
        "tag": tag,
        "tags": tags,
        "seach_regex": seach_regex,
        "exit": exits
    }

    result = user_input.split(": ")

    if result[0] in command.keys():
        result = command[result[0]](" ".join(result[1:]))

    return result


def main():
    while True:
        try:
            user_input = input('>>> Write command with value: ')
            result = hadlde_command(user_input)
            print(result)
        except KeyboardInterrupt as err:
            print(err)
            exits()


if __name__ == "__main__":
    main()