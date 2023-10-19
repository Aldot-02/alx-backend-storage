import requests
import time
from functools import wraps

# Cache to store results with expiration time
cache = {}

def get_page(url):
    cache_key = f"count:{url}"
    
    # Check if the result is already in cache
    if cache.get(cache_key) and time.time() - cache[cache_key]['timestamp'] < 10:
        cache[cache_key]['count'] += 1
        return cache[url]['content']
    
    # If not in cache, fetch the page
    response = requests.get(url)
    content = response.text
    
    # Update cache with new result
    cache[cache_key] = {
        'content': content,
        'timestamp': time.time(),
        'count': 1
    }
    
    return content

# Bonus: Implementing a decorator for caching
def cache_decorator(func):
    cache = {}
    
    @wraps(func)
    def wrapper(url):
        cache_key = f"count:{url}"
        
        if cache.get(cache_key) and time.time() - cache[cache_key]['timestamp'] < 10:
            cache[cache_key]['count'] += 1
            return cache[url]['content']
        
        response = func(url)
        cache[cache_key] = {
            'content': response,
            'timestamp': time.time(),
            'count': 1
        }
        
        return response
    
    return wrapper

@cache_decorator
def get_page_with_cache(url):
    return requests.get(url).text
