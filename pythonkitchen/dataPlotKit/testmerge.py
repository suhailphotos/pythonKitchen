import os
import pandas as pd

def merge_data():
    project_root = os.environ.get('PROJECT_ROOT')
    netflix_path = f'{project_root}/data/netflix_titles.csv'
    tmdb_path = f'{project_root}/data/TMDb_updated.CSV'
    netflix_data = pd.read_csv(netflix_path)
    tmdb_data = pd.read_csv(tmdb_path)
    
    # Rename columns in tmdb_data to avoid suffixes
    tmdb_data = tmdb_data.rename(columns={
        'overview': 'overview_imdb',
        'original_language': 'original_language_imdb',
        'vote_count': 'vote_count_imdb',
        'vote_average': 'vote_average_imdb'
    })
    
    # Merge the datasets
    merged_data = pd.merge(netflix_data, tmdb_data, on='title')
    print(merged_data.head())

merge_data()

