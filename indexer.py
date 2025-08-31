# Builds inverted index


# indexer.py
import csv
import string
import pickle
from collections import defaultdict

# -------------------------
# Step 1: Load publications
# -------------------------
def load_publications(csv_path):
    publications = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            publications.append(row)
    print(f"[info] Loaded {len(publications)} publications.")
    return publications

# -------------------------
# Step 2: Pre-process text
# -------------------------
def preprocess(text):
    text = text.lower()  # lowercase
    text = text.translate(str.maketrans("", "", string.punctuation))  # remove punctuation
    words = text.split()
    stopwords = {"the", "and", "of", "in", "on", "for", "a", "an", "with", "to"}
    words = [w for w in words if w not in stopwords]
    return words

# -------------------------
# Step 3: Build inverted index
# -------------------------
def build_inverted_index(publications):
    inverted_index = defaultdict(list)
    for idx, pub in enumerate(publications):
        words = preprocess(pub["title"])
        for word in words:
            inverted_index[word].append(idx)
    print(f"[info] Inverted index built with {len(inverted_index)} unique words.")
    return inverted_index

# -------------------------
# Step 4: Save inverted index
# -------------------------
def save_index(inverted_index, filepath="data/inverted_index.pkl"):
    with open(filepath, "wb") as f:
        pickle.dump(inverted_index, f)
    print(f"[info] Inverted index saved to {filepath}")

# -------------------------
# Main function
# -------------------------
def main():
    csv_path = r"E:\Information_Retrieval_Assignment\data\publications.csv"
    publications = load_publications(csv_path)
    inverted_index = build_inverted_index(publications)
    save_index(inverted_index)

if __name__ == "__main__":
    main()
