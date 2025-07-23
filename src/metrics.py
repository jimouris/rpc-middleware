"""Metrics tracking provider usage counts."""
from threading import Lock
from typing import Dict


class Metrics:
    """Tracks usage counts for each provider."""

    def __init__(self):
        """Initialize the metrics storage and lock."""
        self.usage: Dict[str, int] = {}
        self.lock = Lock()

    def increment(self, provider_name: str):
        """Increment the usage count for a given provider name."""
        with self.lock:
            if provider_name not in self.usage:
                self.usage[provider_name] = 0
            self.usage[provider_name] += 1

    def get_usage(self) -> Dict[str, int]:
        """Return a copy of the current usage counts for all providers."""
        with self.lock:
            return dict(self.usage)
