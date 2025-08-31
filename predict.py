import joblib
import numpy as np
# Paths
DATA_DIR = "E:/Information_Retrieval_Assignment/Task_2_Classifier/data"

# Load model and BERT
clf = joblib.load(f"{DATA_DIR}/news_classifier_bert.pkl")
bert_model = joblib.load(f"{DATA_DIR}/bert_model.pkl")
# Minimum confidence threshold
CONF_THRESHOLD = 0.35

# User input loop
while True:
    text = input("\nEnter a news headline (or 'exit' to quit): ")
    if text.lower() == "exit":
        break
    if len(text.strip()) < 1:
        print("⚠️ Please enter some text!")
        continue

    # Generate embedding
    emb = bert_model.encode([text])
    proba = clf.predict_proba(emb)[0]
    pred_idx = np.argmax(proba)
    confidence = proba[pred_idx]
    category = clf.classes_[pred_idx]

    if confidence < CONF_THRESHOLD:
        # Show top-2 predictions
        top2_idx = np.argsort(proba)[-2:][::-1]
        top2 = [(clf.classes_[i], proba[i]) for i in top2_idx]
        print(f"Low confidence ({confidence:.2f}) prediction. Top predictions:")
        for cat, conf in top2:
            print(f"   - {cat}: {conf:.2f}")
    else:
        print(f"Predicted Category: {category} (confidence: {confidence:.2f})")
