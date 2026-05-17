import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

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