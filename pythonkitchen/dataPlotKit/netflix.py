import time, os
from fuzzywuzzy import fuzz, process
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
from tqdm import tqdm

class Netlix:
    def __init__(self, netflix_dataset: str, tmdb_dataset: str, tmdb_top_1000: str, threshold: int = 90, force_cache: bool = False, cache_path: str = None):
        self.netflix_dataset = pd.read_csv(netflix_dataset)
        self.tmdb_dataset = pd.read_csv(tmdb_dataset)
        self.tmdb_top_1000 = pd.read_csv(tmdb_top_1000)
        self.threshold = threshold
        self.force_cache = force_cache
        netflix_col_ren_mapping = {
                column: f'{column}_netflix' for column in self.netflix_dataset.columns if column != 'title'
                }
        tmdb_col_ren_mapping = {
                column: 'title' if column == 'names' else f'{column}_tmdb' 
                for column in self.tmdb_dataset.columns
                }
        tmdb_top_1000_mapping = {
                column: f'{column}_top_1000' for column in self.tmdb_top_1000.columns if column != 'title'
                }
        self.netflix_dataset = self.netflix_dataset.rename(columns=netflix_col_ren_mapping)
        self.tmdb_dataset = self.tmdb_dataset.rename(columns=tmdb_col_ren_mapping)
        self.tmdb_top_1000 = self.tmdb_top_1000.rename(columns=tmdb_top_1000_mapping)
        self.tmdb_dataset_combined = pd.merge(self.tmdb_dataset, self.tmdb_top_1000, on='title', how='inner')
        self.tmdb_dataset_combined.to_csv(f'{os.environ.get('PROJECT_ROOT')}/data/tmdb_merge.csv')


if __name__=='__main__':
    project_root = os.environ.get('PROJECT_ROOT')
    netflix_dataset = f'{project_root}/data/netflix_titles.csv'
    tmdb_dataset = f'{project_root}/data/imdb_movies.csv'
    tmdb_top_1000 = f'{project_root}/data/TMDb_top_1000.CSV'
    n = Netlix(netflix_dataset, tmdb_dataset, tmdb_top_1000, 90, False)



