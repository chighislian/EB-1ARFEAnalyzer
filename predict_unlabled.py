#This script will:
	#1.	Load your trained classifier and vectorizer (classifier_model.joblib and tfidf_vectorizer.joblib)
	#2.	Go through every .json file in the output_json/ folder
	#3.	Check if a red flag pattern is missing a criterion label
	#4.	Use your model to predict the correct criterion
	#5.	Add the predicted criterion to that red flag entry
	#6.	Save the updated JSON back to the same file

import os
import json
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer

# Load model and vectorizer
model = load("model/classifier_model.joblib")
vectorizer = load("model/tfidf_vectorizer.joblib")

# Folder containing JSON files from analyze_petition.py
INPUT_FOLDER = "petition_analysis"

# Walk through all .json files
for filename in os.listdir(INPUT_FOLDER):
    if not filename.endswith(".json"):
        continue

    filepath = os.path.join(INPUT_FOLDER, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    changed = False

    for section_name, red_flags in data.get("sections", {}).items():
        for item in red_flags:
            if not item.get("criterion"):
                phrase = item["pattern"]
                X = vectorizer.transform([phrase])
                predicted_label = model.predict(X)[0]
                item["criterion"] = predicted_label
                changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

print("✅ All unlabeled red flags have been classified and updated.")