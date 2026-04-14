"""
limit = 5 requests
window = 10 seconds
"""

#1️⃣ Fixed Window Counter -> Count requests in a fixed time window.

from abc import ABC, abstractmethod
from asyncio import Lock
import time
from collections import defaultdict

class RateLimiter(ABC):
    @abstractmethod
    def allow_request(self, userId: str) -> bool:
        pass

class FixedWindowRateLimiter(RateLimiter):
    def __init__(self, limit: int, window_size: int):
        self.limit = limit
        self.window_size = window_size
        self.counters = defaultdict(int)
        self.window_start = defaultdict(int)

    def allow_request(self, user_id: str) -> bool:
        current_time = int(time.time())
        window = current_time // self.window_size

        if self.window_start[user_id] != window:
            self.window_start[user_id] = window
            self.counters[user_id] = 0

        if self.counters[user_id] < self.limit:
            self.counters[user_id] += 1
            return True
        return False
    

#2️⃣ Sliding Window Log -> Store timestamps of every request, Always check last N seconds.
from collections import deque

class SlidingWindowLogRateLimiter(RateLimiter):
    def __init__(self, limit: int, window_size: int):
        self.limit = limit
        self.window_size = window_size
        self.logs = defaultdict(deque)

    def allow_request(self, user_id: str) -> bool:
        now = time.time()
        q = self.logs[user_id]

        while q and q[0] <= now - self.window_size:
            q.popleft()

        if len(q) < self.limit:
            q.append(now)
            return True
        return False
    

#3️⃣ Sliding Window Counter -> Keep counts of current + previous window
# Effective count = (previous window request * overlap %) + current window requests

class SlidingWindowCounterRateLimiter(RateLimiter):
    def __init__(self, limit: int, window_size: int):
        self.limit = limit
        self.window_size = window_size
        self.current_window = defaultdict(int)
        self.previous_window = defaultdict(int)
        self.window_start = int(time.time())

    def allow_request(self, user_id: str) -> bool:
        now = time.time()
        if now - self.window_start >= self.window_size:
            self.previous_window = self.current_window
            self.current_window = defaultdict(int)
            self.window_start = now

        elapsed = now - self.window_start
        overlap = (self.window_size - elapsed) / self.window_size

        total = (self.previous_window[user_id] * overlap) + self.current_window[user_id]

        if total < self.limit:
            self.current_window[user_id] += 1
            return True
        return False


#4️⃣ Token Bucket -> Tokens refill at fixed rate, Each request consumes 1 token.
#**Most Important
class TokenBucketRateLimiter(RateLimiter):
    def __init__(self, capacity = 5, refill_rate = 1):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = defaultdict(lambda: self.capacity)
        self.last_refill_time = defaultdict(lambda : time.time())
        self.lock = Lock()

    def refill(self, userId):
        current_time = time.time()
        elapsed = current_time - self.last_refill_time[userId]
        new_tokens = self.refill_rate * elapsed 
        self.tokens[userId] = min(self.capacity, self.tokens[userId] + new_tokens)
        self.last_refill_time[userId] = current_time
    
    def allow_request(self, userId, required_tokens = 1):
        with self.lock:
            self.refill(userId)
            if self.tokens[userId] >= (required_tokens + 1e-6):
                self.tokens[userId] -= required_tokens
                return True 
            return False 
    
    def getAvailableTokens(self, userId):
        with self.lock:
            self.refill(userId)
            return int(self.tokens[userId] + 1e-6)
        

