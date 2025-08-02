# predict_labels.py

#This script will:
	#•	Load your trained classifier and vectorizer
	#•	Accept new phrases (manually or from a file)
	#•	Predict the EB-1A criterion label for each one
	#•	Print or save the predictions



import joblib

# === Load from model folder ===
model = joblib.load("model/classifier_model.joblib")
vectorizer = joblib.load("model/tfidf_vectorizer.joblib")

# === Test phrases ===
red_flag_phrases = [
    "no evidence award is recognized by peers in the field",
    "articles not published in peer-reviewed journals",
    "no third-party validation of achievements",
    "financial data is self-reported without verification"
]

X_new = vectorizer.transform(red_flag_phrases)
predictions = model.predict(X_new)

# === Output ===
for phrase, label in zip(red_flag_phrases, predictions):
    print(f"Phrase: {phrase}\nPredicted Criterion: {label}\n")