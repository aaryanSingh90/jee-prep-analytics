import pandas as pd
import joblib
import os

# ---------- CONFIG ----------
INPUT_FILE = "/Users/aaryansingh/Desktop/question_Prediction/data/transformed_dataset.csv"

MODEL_DIR = "/Users/aaryansingh/Desktop/question_Prediction/models"

OUTPUT_FILE = "/Users/aaryansingh/Desktop/question_Prediction/output/finalDataSheet/predicted_questions.csv"


# ---------- LOAD DATA ----------
df = pd.read_csv(INPUT_FILE)

# Rename if needed
df = df.rename(columns={
    "question_text": "question",
    "correct_option": "answer"
})

# ---------- LOAD SUBJECT MODEL ----------
subject_model = joblib.load(
    os.path.join(MODEL_DIR, "subject_model.pkl")
)

# ---------- PREDICT SUBJECT ----------
df["subject"] = subject_model.predict(df["question"])

# ---------- LOAD UNIT MODELS ----------
unit_models = {}

for subject in df["subject"].unique():
    model_path = os.path.join(
        MODEL_DIR,
        f"unit_model_{subject}.pkl"
    )
    unit_models[subject] = joblib.load(model_path)

# ---------- PREDICT UNIT ----------
unit_preds = []

for _, row in df.iterrows():
    model = unit_models[row["subject"]]
    pred = model.predict([row["question"]])[0]
    unit_preds.append(pred)

df["unit_name"] = unit_preds

# ---------- CREATE GLOBAL QID ----------
df = df.reset_index(drop=True)
df["global_qid"] = df.index + 1

# ---------- FINAL COLUMN FORMAT ----------
final_df = df[[
    "global_qid",
    "exam_session",
    "year",
    "subject",
    "unit_name",
    "question",
    "options",
    "answer"
]]

# ---------- SAVE ----------
final_df.to_csv(OUTPUT_FILE, index=False)

print("\n✅ Prediction complete")
print("Saved file:", OUTPUT_FILE)
print("Total questions:", len(final_df))
