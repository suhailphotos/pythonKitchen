from fuzzywuzzy import fuzz, process
import pandas as pd
import os

class Netflix:
    def __init__(self, netflix_dataset: str, other_dataset: str, output_csv: str):
        self.netflix_data = pd.read_csv(netflix_dataset)
        self.other_data = pd.read_csv(other_dataset)
        self.combined_data = pd.merge(self.netflix_data, self.other_data, on='title', how='inner')
        self.output_csv = output_csv
        self.mismatches = self._find_mismatches()

    def _find_mismatches(self, threshold=90):
        merged_titles = self.combined_data['title'].unique()
        unmatched_titles = self.netflix_data[~self.netflix_data['title'].isin(merged_titles)]['title']
        imdb_titles = self.other_data['title'].unique()
        mismatches = []
        for title in unmatched_titles:
            matches = process.extractOne(title, imdb_titles, scorer=fuzz.ratio)
            if matches and matches[1] >= threshold:
                mismatches.append((title, matches[0], matches[1]))
        
        # Save mismatches to CSV
        mismatches_df = pd.DataFrame(mismatches, columns=['Netflix Title', 'IMDb Title', 'Similarity Score'])
        mismatches_df.to_csv(self.output_csv, index=False)
        
        return mismatches

if __name__ == "__main__":
    project_root = os.environ.get('PROJECT_ROOT')
    netflix_path = f'{project_root}/data/netflix_titles.csv'
    tmdb_path = f'{project_root}/data/TMDb_updated.CSV'
    output_csv = f'{project_root}/data/mismatches.csv'
    
    n = Netflix(netflix_path, tmdb_path, output_csv)
    print("Mismatches saved to mismatches.csv")
 
    

