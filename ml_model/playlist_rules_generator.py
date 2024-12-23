import pandas as pd
from fpgrowth_py import fpgrowth
import pickle
from collections import Counter
from datetime import datetime


MIN_SUPPORT = 0.06  
MIN_CONFIDENCE = 0.5  

model_path = "/app/model/recommendation_model.pkl"

def train_model():
    data = pd.read_csv('2023_spotify_ds1.csv')
    transactions = data.groupby('pid')['track_name'].apply(list).tolist()
    _, rules = fpgrowth(transactions, minSupRatio=MIN_SUPPORT, minConf=MIN_CONFIDENCE)
    # Calcular a popularidade das faixas
    all_tracks = data['track_name'].tolist()
    track_counts = Counter(all_tracks)
    last_update_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(model_path, 'wb') as f:
        pickle.dump((rules, track_counts, last_update_date), f)


train_model()

