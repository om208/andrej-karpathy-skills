import pandas as pd
import numpy as np
from datetime import datetime

class DataLoader:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df['datetime'] = pd.to_datetime(self.df['datetime'])
        self.df = self.df.sort_values('datetime').reset_index(drop=True)

    def get_data(self):
        return self.df.copy()

    def get_summary(self):
        return {
            'total_candles': len(self.df),
            'start_date': self.df['datetime'].min(),
            'end_date': self.df['datetime'].max(),
            'price_range': (self.df['close'].min(), self.df['close'].max()),
            'avg_volume': self.df['volume'].mean()
        }
