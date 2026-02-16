import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_PATH = "/Users/aaryansingh/Desktop/question_Prediction/output/finalDataSheet/predicted_questions.csv"

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

questions = df["question"].fillna("").tolist()

print("Building TF-IDF index...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=150000,
    ngram_range=(1,2)
)

tfidf_matrix = vectorizer.fit_transform(questions)

joblib.dump(vectorizer, "recommender_vectorizer.pkl")
joblib.dump(tfidf_matrix, "question_vectors.pkl")
joblib.dump(df, "question_dataframe.pkl")

print("✅ Recommendation index built.")
