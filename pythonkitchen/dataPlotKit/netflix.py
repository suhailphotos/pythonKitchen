from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import os

class Netflix:
    def __init__(self, netflix_dataset: str, other_dataset: str):
        self.netflix_data = pd.read_csv(netflix_dataset)
        self.other_data = pd.read_csv(other_dataset)
        self.combined_data = pd.merge(self.netflix_data, self.other_data, on='title', how='inner')
        self.mismatches = self._find_mismatches(test_mode=True)

    def _find_mismatches(self, threshold=3, test_mode=False, max_iterations=3000):
        mismatched_titles = []
        unmatched_data = self.other_data[~self.other_data['title'].isin(self.combined_data['title'])]
        iteration_count = 0
        for title1 in self.netflix_data['title']:
            matches = process.extractBests(title1, unmatched_data['title'], scorer=fuzz.ratio, score_cutoff=90)
            for match in matches:
                title2 = match[0]
                distance = fuzz.ratio(title1, title2)
                if distance <= threshold:
                    mismatched_titles.append((title1, title2, distance))
            iteration_count += 1
            if test_mode and iteration_count >= max_iterations:
                break
        return mismatched_titles


if __name__ == "__main__":
    project_root = os.environ.get('PROJECT_ROOT')
    netflix_path = f'{project_root}/data/netflix_titles.csv'
    tmdb_path = f'{project_root}/data/TMDb_updated.CSV'
    n = Netflix(netflix_path, tmdb_path)
    for mismatch in n.mismatches:
        print(mismatch)
         
  
    

