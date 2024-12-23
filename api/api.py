from flask import Flask, request, jsonify
import pickle
from datetime import date

MIN_SUPPORT_THRESHOLD = 0.50
CODE_VERSION = 1.0
SONGS_NUMBER = 7

app = Flask(__name__)

model_path = "/app/model/recommendation_model.pkl"
app.model = pickle.load(open(model_path, "rb"))

def filter_rules_by_confidence(rules, min_confidence):
    filtered_rules = [rule for rule in rules if rule[2] >= min_confidence]
    return filtered_rules

def get_recommendations(user_tracks, num_recommendations=5):
    rules, track_counts, _ = app.model

    filtered_rules = filter_rules_by_confidence(rules, MIN_SUPPORT_THRESHOLD)
    recommendations = set()

    # Tentar gerar recomendações baseadas em regras
    for rule in filtered_rules:
        antecedents = rule[0]
        consequents = rule[1]
        
        if antecedents.issubset(user_tracks):
            recommendations.update(consequents)

    # Remover faixas já ouvidas das recomendações
    recommendations.difference_update(user_tracks)

    # Se não houver recomendações suficientes, usar fallback de popularidade
    if len(recommendations) < num_recommendations:
        most_common_tracks = [track for track, _ in track_counts.most_common() if track not in user_tracks]
        additional_recommendations = most_common_tracks[:num_recommendations - len(recommendations)]
        recommendations.update(additional_recommendations)

    return list(recommendations)[:num_recommendations]



@app.route("/api/recommend", methods=["POST"])
def recommend():
    request_data = request.json
    songs_set = set(request_data["songs"])
    _, _, last_update_date = app.model
    return jsonify(
        {
            "songs": get_recommendations(songs_set, SONGS_NUMBER),
            "version": CODE_VERSION,
            "model_date": last_update_date
        }
    )

 