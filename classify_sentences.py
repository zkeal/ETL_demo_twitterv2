import re
import nltk
from textblob import TextBlob


def preprocessor(sentence):
    sentence = sentence.strip().lower()
    sentence = re.sub(r"\d+", "", sentence)
    sentence = re.sub(r'[^\w\s]', '', sentence)
    sentence = " ".join([w for w in nltk.word_tokenize(sentence) if len(w) > 1])
    return sentence


def classify(sentence):
    sentence = preprocessor(sentence)
    polarity = TextBlob(sentence).sentiment.polarity
    prediction = "Positive" if polarity >= 0 else "Negative"
    return prediction
