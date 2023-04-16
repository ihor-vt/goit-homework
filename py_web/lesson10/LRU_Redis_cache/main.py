import redis
from redis_lru import RedisLRU
import timeit
from functools import lru_cache

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


@cache
def fibonacci_cache(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_cache(n - 1) + fibonacci_cache(n - 2)


@lru_cache
def fibonacci_cache_lru(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_cache_lru(n - 1) + fibonacci_cache_lru(n - 2)


start_time = timeit.default_timer()
fibonacci(38)
print(f'Duration with cache: {timeit.default_timer() - start_time}')  # 21.598374299996067

start_time = timeit.default_timer()
fibonacci_cache(500)
print(f'Duration with Redis cache: {timeit.default_timer() - start_time}')  # 2.5674591999850236

start_time = timeit.default_timer()
fibonacci_cache_lru(500)
print(f'Duration with decorator @lru_cache, model functools: {timeit.default_timer() - start_time}')  # 0.00419589999364689
