import pandas as pd
import os

class Netflix:
    def __init__(self, netlix_dataset: str, other_dataset: str):
        self.netflix_data = pd.read_csv(netlix_dataset)
        self.other_data = pd.read_csv(other_dataset)
        self.combined_data = pd.merge(self.netflix_data, self.other_data, on='title', how='inner')
        print(f'Netflix data size: {len(self.netflix_data)}')
        print(f'IMDb data size: {len(self.other_data)}')
        self._find_mismaches(threshold=90)

    def _find_mismaches(self, threshold=90):
        mismatched_titles = []
        unmatched_data = self.other_data[~self.other_data['title'].isin(self.combined_data['title'])]
        print(f'Unmatched_titles: {len(unmatched_data)}')



if __name__ == "__main__":
    project_root = os.environ.get('PROJECT_ROOT')
    netflix_path = f'{project_root}/data/netflix_titles.csv'
    tmdb_path = f'{project_root}/data/TMDb_updated.CSV'
    n = Netflix(netflix_path, tmdb_path)
       
  
    

