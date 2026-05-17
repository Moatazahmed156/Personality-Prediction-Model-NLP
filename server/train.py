import pandas as pd
import numpy as np
import re
import pickle
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Download NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# -------------------------------
# 1. Load Dataset
# -------------------------------
df = pd.read_csv("mbti_1.csv")

# -------------------------------
# 2. Preprocessing
# -------------------------------
def clean_text(text):
    text = text.lower()
    text = text.replace("|||", " ")

    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    mbti_types = [
        'infj','infp','intj','intp','isfj','isfp','istj','istp',
        'enfj','enfp','entj','entp','esfj','esfp','estj','estp'
    ]
    for t in mbti_types:
        text = text.replace(t, '')

    text = re.sub(r'[^a-z\s]', '', text)

    words = text.split()
    words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)

print("Cleaning text...")
df["clean_posts"] = df["posts"].apply(clean_text)

# -------------------------------
# 3. Feature Extraction
# -------------------------------
print("Vectorizing...")
tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1,2))

X = tfidf.fit_transform(df["clean_posts"])
y = df["type"]

# -------------------------------
# 4. Train/Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------
# 5. Train Model
# -------------------------------
print("Training model...")
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train, y_train)

# -------------------------------
# 6. Evaluate
# -------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("✅ Accuracy:", accuracy)

# -------------------------------
# 7. Save Model
# -------------------------------
print("Saving model...")

with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("model/vectorizer.pkl", "wb") as f:
    pickle.dump(tfidf, f)

print("🎉 Model and vectorizer saved successfully!")