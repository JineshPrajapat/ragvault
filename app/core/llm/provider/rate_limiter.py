import asyncio
import time
from .rate_limits import GEMINI_RPM


class RateLimiter:

    def __init__(self):

        self.requests = []
        self.max_requests = GEMINI_RPM

    async def wait_if_needed(self):

        now = time.time()

        self.requests = [
            r for r in self.requests
            if now - r < 60
        ]

        print(f"Requests in the last 60 seconds: {len(self.requests)}")

        if len(self.requests) >= self.max_requests:

            sleep_time = 60 - (now - self.requests[0])
            print(f"Rate limit exceeded. Sleeping for {sleep_time:.2f} seconds.")
            await asyncio.sleep(sleep_time)

        self.requests.append(time.time())