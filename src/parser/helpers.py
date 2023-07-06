import functools
import time

from django.db import reset_queries, connection


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_count_queries = len(connection.queries)
        start_time = time.perf_counter()
        result = func(*args, *kwargs)
        end_time = time.perf_counter()
        end_count_queries = len(connection.queries)

        print(f'Function - {func.__name__}')
        print(f'Queries count = {end_count_queries - start_count_queries}')
        print(f'Time - {(end_time - start_time):.2f}s')
        return result
    return inner_func
