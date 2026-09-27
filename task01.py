import random
import time
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

def range_sum_no_cache(array, left, right):
    return sum(array[left:right + 1])

def update_no_cache(array, index, value):
    array[index] = value

def range_sum_with_cache(array, left, right, cache):
    key = (left, right)
    result = cache.get(key)
    if result == -1:
        result = sum(array[left:right + 1])
        cache.put(key, result)
    return result

def update_with_cache(array, index, value, cache):
    array[index] = value
    keys_to_delete = []
    for key in cache.cache.keys():
        left, right = key
        if left <= index <= right:
            keys_to_delete.append(key)
    
    for key in keys_to_delete:
        del cache.cache[key]

def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n // 2), random.randint(n // 2, n - 1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries

if __name__ == "__main__":
    N = 100_000
    Q = 50_000
    
    # Генерація даних
    array_no_cache = [random.randint(1, 100) for _ in range(N)]
    array_with_cache = array_no_cache.copy()
    queries = make_queries(N, Q)
    
    # Тестування без кешу
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(array_no_cache, query[1], query[2])
        else:
            update_no_cache(array_no_cache, query[1], query[2])
    no_cache_time = time.time() - start_time
    
    # Тестування з LRU-кешем
    lru_cache = LRUCache(1000)
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_with_cache(array_with_cache, query[1], query[2], lru_cache)
        else:
            update_with_cache(array_with_cache, query[1], query[2], lru_cache)
    with_cache_time = time.time() - start_time
    
    # Вивід результатів
    print(f"Без кешу\t: {no_cache_time:>6.2f} с")
    print(f"LRU-кеш\t\t: {with_cache_time:>6.2f} с")