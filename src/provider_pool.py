import csv
import random
from typing import List

class Provider:
    def __init__(self, name: str, url: str, weight: int):
        self.name = name
        self.url = url
        self.weight = weight

    def __repr__(self):
        return f"Provider(name={self.name}, url={self.url}, weight={self.weight})"

class ProviderPool:
    def __init__(self, csv_path: str):
        self.providers: List[Provider] = []
        self.weights: List[int] = []
        self.load_providers(csv_path)

    def load_providers(self, csv_path: str):
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['name']
                url = row['url']
                weight = int(row.get('weight', 1))
                provider = Provider(name, url, weight)
                self.providers.append(provider)
                self.weights.append(weight)

    def get_random_provider(self) -> Provider:
        return random.choices(self.providers, weights=self.weights, k=1)[0]
