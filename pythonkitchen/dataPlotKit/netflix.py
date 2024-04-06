from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import os

class Netflix:
    def __init__(self, netlix_dataset: str, other_dataset: str):
        self.netflix_data = pd.read_csv(netlix_dataset)
        self.other_data = pd.read_csv(other_dataset)
        self.combined_data = pd.merge(self.netflix_data, self.other_data, on='title', how='inner')

    def find_potential_mismatches(self, threshold=90):
        mismatched_titles = []
        for title1 in self.combined_data['title']:
            matches = process.extract(title1, self.combined_data['title'], scorer=fuzz.partial_ratio)
            print(matches)

if __name__ == "__main__":
    netflix_path = f'{os.environ.get('PROJECT_ROOT')}/data/netflix_titles.csv'
    print(netflix_path)
  
    

