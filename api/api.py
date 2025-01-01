from flask import Flask, request, jsonify
import pickle
from datetime import date
import os
from flask_cors import CORS


MIN_SUPPORT_THRESHOLD = 0.3
SONGS_NUMBER = 5

app = Flask(__name__)
CORS(app)  

model_path = "/app/model/recommendation_model.pkl"

os.makedirs(os.path.dirname(model_path), exist_ok=True)


last_known_update_date = None

def load_model():
    global last_known_update_date
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)

    _, _, last_update_date, _ = model_data
    
    if last_known_update_date != last_update_date:
        print("Modelo atualizado. Recarregando...")
        last_known_update_date = last_update_date
        app.model = model_data




def filter_rules_by_confidence(rules, min_confidence):
    filtered_rules = [rule for rule in rules if rule[2] >= min_confidence]
    return filtered_rules



def get_recommendations(user_tracks, num_recommendations=5):
    rules, track_counts, _, _ = app.model

    filtered_rules = filter_rules_by_confidence(rules, MIN_SUPPORT_THRESHOLD)
    recommendations = set()

    for rule in filtered_rules:
        antecedents = rule[0]
        consequents = rule[1]
        
        if antecedents.issubset(user_tracks):
            recommendations.update(consequents)

    recommendations.difference_update(user_tracks)
    print("recomendações baseadas nas regras", recommendations)
    if len(recommendations) < num_recommendations:
        most_common_tracks = [track for track, _ in track_counts.most_common() if track not in user_tracks]
        additional_recommendations = most_common_tracks[:num_recommendations - len(recommendations)]
        print("recomendações músicas mais populares", additional_recommendations)
        recommendations.update(additional_recommendations)

    return list(recommendations)[:num_recommendations]



@app.route("/api/recommend", methods=["POST"])
def recommend():
    request_data = request.json
    songs_set = set(request_data["songs"])

    load_model()

    _, _, last_update_date, version = app.model
    return jsonify(
        {
            "songs": get_recommendations(songs_set, SONGS_NUMBER),
            "version": version,
            "model_date": last_update_date
        }
    )

if __name__ == '__main__':
    load_model()
    app.run(host='0.0.0.0', port=5008)

