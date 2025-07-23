from typing import Dict
from threading import Lock

class Metrics:
    def __init__(self):
        self.usage: Dict[str, int] = {}
        self.lock = Lock()

    def increment(self, provider_name: str):
        with self.lock:
            if provider_name not in self.usage:
                self.usage[provider_name] = 0
            self.usage[provider_name] += 1

    def get_usage(self) -> Dict[str, int]:
        with self.lock:
            return dict(self.usage)
