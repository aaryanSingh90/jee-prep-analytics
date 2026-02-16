import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import os

# -------- CONFIG --------
DATA_PATH = "/Users/aaryansingh/Desktop/question_Prediction/output/combined/jee_combined_all_sessions2025.csv"
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# -------- LOAD DATA --------
df = pd.read_csv(DATA_PATH)

df = df.dropna(subset=["question_text", "subject", "unit_name"])

X = df["question_text"]
y_subject = df["subject"]

# -------- TRAIN SUBJECT MODEL --------
X_train, X_test, ys_train, ys_test = train_test_split(
    X, y_subject, test_size=0.2, random_state=42
)

subject_model = Pipeline([
    ("tfidf", TfidfVectorizer(
        stop_words="english",
        max_features=150000,
        ngram_range=(1,2)
    )),
    ("clf", LogisticRegression(
        max_iter=1500,
        class_weight="balanced"
    ))
])

subject_model.fit(X_train, ys_train)

subject_pred = subject_model.predict(X_test)
subject_acc = accuracy_score(ys_test, subject_pred)

joblib.dump(subject_model, f"{MODEL_DIR}/subject_model.pkl")

# -------- TRAIN UNIT MODELS PER SUBJECT --------
unit_models = {}
unit_accuracy = {}

for subject in df["subject"].unique():

    sub_df = df[df["subject"] == subject]

    X_sub = sub_df["question_text"]
    y_sub_unit = sub_df["unit_name"]

    if len(sub_df) < 50:
        continue

    X_train_u, X_test_u, y_train_u, y_test_u = train_test_split(
        X_sub, y_sub_unit, test_size=0.2, random_state=42
    )

    unit_model = Pipeline([
        ("tfidf", TfidfVectorizer(
            stop_words="english",
            max_features=150000,
            ngram_range=(1,2)
        )),
        ("clf", LogisticRegression(
            max_iter=1500,
            class_weight="balanced"
        ))
    ])

    unit_model.fit(X_train_u, y_train_u)

    preds = unit_model.predict(X_test_u)
    acc = accuracy_score(y_test_u, preds)

    unit_accuracy[subject] = acc
    unit_models[subject] = unit_model

    joblib.dump(unit_model, f"{MODEL_DIR}/unit_model_{subject}.pkl")

# -------- FINAL ACCURACY --------
print("\n===== MODEL RESULTS =====")
print(f"Subject Accuracy : {subject_acc*100:.2f}%")

print("\nUnit Accuracy per Subject:")
for sub, acc in unit_accuracy.items():
    print(f"{sub}: {acc*100:.2f}%")

avg_unit_acc = sum(unit_accuracy.values()) / len(unit_accuracy)
print(f"\nAverage Unit Accuracy: {avg_unit_acc*100:.2f}%")

# -------- TEST INTERFACE --------
while True:
    question = input("\nEnter a question (or type exit):\n")

    if question.lower() == "exit":
        break

    pred_subject = subject_model.predict([question])[0]

    unit_model = joblib.load(
        f"{MODEL_DIR}/unit_model_{pred_subject}.pkl"
    )

    pred_unit = unit_model.predict([question])[0]

    print("\nPrediction:")
    print("Subject :", pred_subject)
    print("Unit    :", pred_unit)
