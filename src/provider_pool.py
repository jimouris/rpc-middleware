"""Provider pool logic for loading and selecting Ethereum RPC providers."""
import csv
import random
from typing import List


class Provider:
    """Represents an Ethereum RPC provider with a name, URL, and weight."""
    def __init__(self, name: str, url: str, weight: int):
        """Initialize a provider with name, url, and weight."""
        self.name = name
        self.url = url
        self.weight = weight

    def __repr__(self):
        """Return a string representation of the provider."""
        return f"Provider(name={self.name}, url={self.url}, weight={self.weight})"

class ProviderPool:
    """Manages a pool of Ethereum RPC providers and selects one at random."""
    def __init__(self, csv_path: str):
        """Load providers from a CSV file at the given path."""
        self.providers: List[Provider] = []
        self.weights: List[int] = []
        self.load_providers(csv_path)

    def load_providers(self, csv_path: str):
        """Load providers and their weights from a CSV file."""
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['name']
                url = row['url']
                weight = int(row.get('weight', 1))
                provider = Provider(name, url, weight)
                self.providers.append(provider)
                self.weights.append(weight)

    def get_random_provider(self) -> Provider:
        """Return a randomly selected provider, weighted by their assigned weights."""
        return random.choices(self.providers, weights=self.weights, k=1)[0]

    def get_all_providers(self) -> List[Provider]:
        """Return a list of all loaded providers."""
        return self.providers
