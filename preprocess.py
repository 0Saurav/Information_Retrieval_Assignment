import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os

nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("punkt")

DATA_DIR = "E:/Information_Retrieval_Assignment/Task_2_Classifier/data"

df = pd.read_csv(os.path.join(DATA_DIR, "raw_text.csv"))
print("Available columns:", df.columns.tolist())

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return " ".join(tokens)

df["clean_text"] = df["text"].apply(clean_text)

processed_file = os.path.join(DATA_DIR, "processed_text.csv")
df.to_csv(processed_file, index=False, encoding="utf-8")
print(f"✅ Preprocessing complete! Saved to {processed_file}")
