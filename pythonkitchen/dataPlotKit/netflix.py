import pandas as pd
import os

class Netflix:
    def __init__(self, netlix_dataset: str, other_dataset: str):
        self.netflix_data = pd.read_csv(netlix_dataset)
        self.other_data = pd.read_csv(other_dataset)
        self.combined_data = pd.merge(self.netflix_data, self.other_data, on='title', how='inner')


if __name__ == "__main__":
    project_root = os.environ.get('PROJECT_ROOT')
    netflix_path = f'{project_root}/data/netflix_titles.csv'
    tmdb_path = f'{project_root}/data/TMDb_updated.CSV'
    n = Netflix(netflix_path, tmdb_path)
    print(len(n.netflix_data))
    print(len(n.other_data))
    print(len(n.combined_data))
   
  
    

