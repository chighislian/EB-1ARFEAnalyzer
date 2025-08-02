import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load your labeled training data
df = pd.read_csv("training_data.csv")

# Split into input (X) and labels (y)
X = df['text']
y = df['label']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text to TF-IDF vectors
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a simple classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_tfidf, y_train)

# Evaluate
y_pred = clf.predict(X_test_tfidf)
print(classification_report(y_test, y_pred))

# Save the model + vectorizer
joblib.dump(clf, "model/classifier_model.joblib")
joblib.dump(vectorizer, "model/tfidf_vectorizer.joblib")

print("✅ Model and vectorizer saved.")