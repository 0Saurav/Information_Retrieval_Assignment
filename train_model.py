import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load preprocessed data
df = pd.read_csv("E:/Information_Retrieval_Assignment/Task_2_Classifier/data/processed_text.csv")
X = df["clean_text"].astype(str)
y = df["category"]
# Split train-test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# Load BERT model (all-mpnet-base-v2 is fast and high-quality)
bert_model = SentenceTransformer('all-mpnet-base-v2')
# Convert text to embeddings
print("Generating embeddings...")
X_train_vec = bert_model.encode(X_train.tolist(), show_progress_bar=True)
X_test_vec = bert_model.encode(X_test.tolist(), show_progress_bar=True)
# Train classifier (Logistic Regression works well for multi-class)
clf = LogisticRegression(max_iter=500, multi_class='multinomial')
clf.fit(X_train_vec, y_train)
# Evaluate
y_pred = clf.predict(X_test_vec)
y_proba = clf.predict_proba(X_test_vec)
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
# Save model & BERT model reference
joblib.dump(clf, "E:/Information_Retrieval_Assignment/Task_2_Classifier/data/news_classifier_bert.pkl")
joblib.dump(bert_model, "E:/Information_Retrieval_Assignment/Task_2_Classifier/data/bert_model.pkl")

print("✅ Model & embeddings saved")
