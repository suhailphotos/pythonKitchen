from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

class Netflix:
    def __init__(self, netlix_dataset: str, other_dataset: str):
        self.netflix_data = pd.read_csv(netlix_dataset)
        self.other_data = pd.read_csv(other_dataset)
        self.combined_data = pd.merge(self.netflix_data, self.other_data, on='title', how='inner')

    def find_potential_mismatches(self, threshold=90):
        mismatched_titles = []
        for title1 in self.combined_data['title']:
            matches = process.extract(title1, self.combined_data['title'], scorer=fuzz.partial_ratio)
            for title2, score in matches:
                if title1 != title2 and score < threshold:
                    mismatched_titles.append((title1, title2, score))
        return mismatched_titles


