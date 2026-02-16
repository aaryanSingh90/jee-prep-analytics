import joblib
from sklearn.metrics.pairwise import cosine_similarity

print("Loading recommender...")

vectorizer = joblib.load("recommender_vectorizer.pkl")
question_vectors = joblib.load("question_vectors.pkl")
df = joblib.load("question_dataframe.pkl")

print("Ready!")

def recommend(question_text, top_k=5):

    query_vec = vectorizer.transform([question_text])

    similarities = cosine_similarity(query_vec, question_vectors)[0]

    top_indices = similarities.argsort()[-top_k-1:][::-1]

    results = []

    for idx in top_indices:
        row = df.iloc[idx]

        results.append({
            "subject": row["subject"],
            "unit": row["unit_name"],
            "year": row["year"],
            "session": row["exam_session"],
            "question": row["question"]
        })

    return results


while True:
    q = input("\nEnter question (or exit):\n")

    if q.lower() == "exit":
        break

    recs = recommend(q)

    print("\nRecommended Questions:\n")

    for i, r in enumerate(recs, 1):
        print(f"{i}. [{r['subject']} - {r['unit']}]")
        print(f"   Asked in: JEE Main {r['session']} {r['year']}")
        print(r["question"][:200], "\n")
