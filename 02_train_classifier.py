

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib  

df = pd.read_csv("transactions.csv")
print(f"Loaded {len(df)} transactions.")
print(df["category"].value_counts())


X = df["description"]
y = df["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
   
)

print(f"\nTraining on {len(X_train)} transactions, testing on {len(X_test)}.")

vectorizer = TfidfVectorizer(lowercase=True, token_pattern=r"[A-Za-z]+")
X_train_vectors = vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_vectors, y_train)

predictions = model.predict(X_test_vectors)
accuracy = accuracy_score(y_test, predictions)

print(f"\nAccuracy on unseen test data: {accuracy:.1%}")
print("\nDetailed breakdown by category:")
print(classification_report(y_test, predictions))

joblib.dump(model, "category_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("\nSaved trained model to category_model.pkl and vectorizer.pkl")

print("\n--- Quick test on new, made-up descriptions ---")
new_examples = ["ZOMATO ORDER 9182", "UBER RIDE HOME", "NETFLIX MONTHLY"]
new_vectors = vectorizer.transform(new_examples)
new_predictions = model.predict(new_vectors)

for desc, pred in zip(new_examples, new_predictions):
    print(f"  '{desc}' -> predicted category: {pred}")
