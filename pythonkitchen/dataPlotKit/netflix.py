import pandas as pd

class Netflix:
    def __init__(self, netlix_dataset: str, other_dataset: str):
        self.netflix_data = pd.read_csv(netlix_dataset)
        self.other_data = pd.read_csv(other_dataset)
        self.combined_data = pd.merge(self.netflix_data, self.other_data, on='title', how='inner')


