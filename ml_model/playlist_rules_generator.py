import pandas as pd
from fpgrowth_py import fpgrowth
import pickle
from collections import Counter
from datetime import datetime
import os


MIN_SUPPORT = 0.05
MIN_CONFIDENCE = 0.4
version = "1.0"  

url = os.getenv("DATASET_URL")

model_path = "/app/model/recommendation_model.pkl"

os.makedirs(os.path.dirname(model_path), exist_ok=True)

def train_model():
    print('executando')
    df = pd.read_csv(url)
    transactions = df.groupby('pid')['track_name'].apply(list).tolist()
    _, rules = fpgrowth(transactions, minSupRatio=MIN_SUPPORT, minConf=MIN_CONFIDENCE)
    all_tracks = df['track_name'].tolist()
    track_counts = Counter(all_tracks)
    last_update_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(model_path, 'wb') as f:
        pickle.dump((rules, track_counts, last_update_date, version), f)


train_model()

