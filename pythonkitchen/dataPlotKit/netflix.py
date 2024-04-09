import time
from fuzzywuzzy import fuzz, process
import pandas as pd
import os
from tqdm import tqdm

class Netflix:
    def __init__(self, netflix_dataset: str, other_dataset: str, threshold: int = 90, force_cache: bool = False, cache_path: str = None):
        self.netflix_data = pd.read_csv(netflix_dataset)
        self.other_data = pd.read_csv(other_dataset)
        self.threshold = threshold
        self.force_cache = force_cache
        self.cache_path = cache_path or os.path.realpath(__file__)  # If cache_path is not provided, use a default cache location
        self.combined_data = pd.merge(self.netflix_data, self.other_data, on='title', how='inner')
        self.find_mismatches()

    def find_mismatches(self):
        if self.force_cache or not os.path.exists(self.cache_path):
            self._cache_mismatches()
            self._append_cache_data(97)
            self.force_cache = False
        else:
            self._append_cache_data(97)

    def _cache_mismatches(self):
        merged_titles = self.combined_data['title'].unique()
        unmatched_titles = self.netflix_data[~self.netflix_data['title'].isin(merged_titles)]['title']
        imdb_titles = self.other_data['title'].unique()
        mismatches = []
        with tqdm(total=len(unmatched_titles)) as pbar:
            for title in unmatched_titles:
                matches = process.extractOne(title, imdb_titles, scorer=fuzz.ratio)
                if matches and matches[1] >= self.threshold:
                    mismatches.append((title, matches[0], matches[1]))
                pbar.update(1) # update process bar
            mismatches_df = pd.DataFrame(mismatches, columns=['Netflix Title', 'IMDb Title', 'Similarity Score'])
            mismatches_df.to_pickle(self.cache_path)

    def _append_cache_data(self, min_similarity_score):
        while not os.path.exists(self.cache_path):
            time.sleep(1)
        mismatches_df = pd.read_pickle(self.cache_path)
        matching_rows = mismatches_df[mismatches_df['Similarity Score'] > min_similarity_score]
        matching_rows = self.other_data[self.other_data['title'].isin(matching_rows['IMDb Title'])]
        self.combined_data = pd.concat([self.combined_data, matching_rows], ignore_index=True)

if __name__ == "__main__":
    project_root = os.environ.get('PROJECT_ROOT')
    netflix_path = f'{project_root}/data/netflix_titles.csv'
    tmdb_path = f'{project_root}/data/TMDb_updated.CSV'
    cache_path = f'{project_root}/data/netflix_cache.pkl'
    
    n = Netflix(netflix_path, tmdb_path, 90, False, cache_path)
 
    

