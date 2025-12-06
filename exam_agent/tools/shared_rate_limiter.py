import time
import threading
from collections import deque

MAX_CALLS = 20
PERIOD_SECONDS = 60.0


class Shared_rate_limiter:
    """A shared thread safe rate limiter"""
    _call_timestamps = deque()
    _rate_limit_lock = threading.Lock()

    @staticmethod
    def clean_up_timestamps():
        """Remove timestamps older than the rate limit period"""
        now = time.monotonic()
        while Shared_rate_limiter._call_timestamps and \
            Shared_rate_limiter._call_timestamps[0] < now - PERIOD_SECONDS :

            Shared_rate_limiter._call_timestamps.popleft()


    @staticmethod
    def get_wait_time():
        """Calculates the necessary waiting time for the next call."""

        with Shared_rate_limiter._rate_limit_lock:
            Shared_rate_limiter._clean_up_timestamps()

            wait_time = 0.0
            if len(Shared_rate_limiter._call_timestamps) >= MAX_CALLS:
                # Calculate time until the oldest timestamp is removed
                time_elapsed = time.monotonic() - Shared_rate_limiter._call_timestamps[0]
                wait_time = PERIOD_SECONDS - time_elapsed
                # Ensure wait_time is non-negative
                wait_time = max(0.0, wait_time)

            return wait_time

    @staticmethod
    def register_call():
        """Registers a new API call."""
        with Shared_rate_limiter._rate_limit_lock:
            Shared_rate_limiter._call_timestamps.append(time.monotonic())
