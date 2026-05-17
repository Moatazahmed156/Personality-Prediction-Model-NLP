from flask import Flask, request, jsonify
import pickle
import numpy as np
from utils.preprocess import clean_text
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend requests

# Load model
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model/vectorizer.pkl", "rb") as f:
    tfidf = pickle.load(f)

PERSONALITY_INFO = {
    "INTJ": {"name": "The Mastermind", "desc": "Strategic visionaries who design long-term systems and solutions."},
    "INTP": {"name": "The Analyst", "desc": "Deep thinkers who explore ideas, logic, and abstract concepts."},
    "ENTJ": {"name": "The Commander", "desc": "Bold leaders who organize people and systems to achieve ambitious goals."},
    "ENTP": {"name": "The Innovator", "desc": "Quick-thinking creators who love debating ideas and exploring possibilities."},

    "INFJ": {"name": "The Visionary", "desc": "Insightful idealists driven by meaning, purpose, and human growth."},
    "INFP": {"name": "The Dreamer", "desc": "Sensitive idealists guided by values, imagination, and empathy."},
    "ENFJ": {"name": "The Mentor", "desc": "Inspiring leaders who empower others to grow and succeed."},
    "ENFP": {"name": "The Explorer", "desc": "Energetic free spirits who chase ideas, experiences, and possibilities."},

    "ISTJ": {"name": "The Inspector", "desc": "Reliable organizers who value order, structure, and responsibility."},
    "ISFJ": {"name": "The Protector", "desc": "Warm caretakers dedicated to supporting and safeguarding others."},
    "ESTJ": {"name": "The Director", "desc": "Efficient organizers who enforce structure and get things done."},
    "ESFJ": {"name": "The Supporter", "desc": "Harmonious caregivers who prioritize people and social balance."},

    "ISTP": {"name": "The Craftsman", "desc": "Practical problem-solvers who excel at hands-on challenges."},
    "ISFP": {"name": "The Artist", "desc": "Gentle creators who express themselves through action and aesthetics."},
    "ESTP": {"name": "The Dynamo", "desc": "Bold, action-oriented individuals who thrive in fast-paced environments."},
    "ESFP": {"name": "The Performer", "desc": "Spontaneous entertainers who bring energy and joy to others."}
}
# Home route
@app.route("/")
def home():
    return jsonify({"message": "MBTI Prediction API is running 🚀"})

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"]

    # Preprocess
    cleaned = clean_text(text)
    features = tfidf.transform([cleaned])

    # Prediction
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)
    confidence = round(np.max(probabilities) * 100, 2)

    info = PERSONALITY_INFO.get(prediction)
    result = {
        "mbti_type": prediction,
        "name": info["name"],
        "description": info["desc"],
        "confidence": f"{confidence}%"
    }

    return jsonify(result)

# Run server
if __name__ == "__main__":
    app.run(debug=True)