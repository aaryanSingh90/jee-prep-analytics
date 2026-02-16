import pandas as pd

# =========================
# CONFIG
# =========================
DATA_PATH = "/Users/aaryansingh/Desktop/question_Prediction/output/finalDataSheet/predicted_questions.csv"
TOTAL_QUESTIONS_PER_PAPER = 25
ROTATION_BOOST = 1.05  # small boost only

# =========================
# LOAD DATA
# =========================
print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

df = df.dropna(subset=["year", "subject", "unit_name"])
df["year"] = df["year"].astype(int)

# =========================
# NORMALIZE CHAPTER NAMES
# =========================
name_map = {
    "Dual Nature": "Modern Physics",
    "Atoms": "Modern Physics",
    "Nuclei": "Nuclear Physics"
}

df["unit_name"] = df["unit_name"].replace(name_map)

# =========================
# USER INPUT
# =========================
start_year = int(input("Start year: "))
end_year = int(input("End year: "))
subject = input("Subject (Physics/Chemistry/Mathematics): ")

df = df[
    (df["year"] >= start_year) &
    (df["year"] <= end_year) &
    (df["subject"] == subject)
]

if df.empty:
    print("No data available.")
    exit()

# =========================
# COUNT PAPERS
# =========================
# Create unique paper ID
df["paper_id"] = df["year"].astype(str) + "_" + df["exam_session"].astype(str)

papers_per_year = df.groupby("year")["paper_id"].nunique()

print("\nPapers per year:")
print(papers_per_year)

# =========================
# QUESTIONS PER PAPER
# =========================
chapter_year_counts = (
    df.groupby(["unit_name", "year"])
    .size()
    .unstack(fill_value=0)
)

chapter_freq = chapter_year_counts.copy()

for year in chapter_freq.columns:
    chapter_freq[year] /= papers_per_year.get(year, 1)

# =========================
# RECENCY WEIGHTS
# =========================
years = sorted(chapter_freq.columns)
weights = {year: i + 1 for i, year in enumerate(years)}

weighted_scores = {}

for chapter, row in chapter_freq.iterrows():
    score = 0
    weight_sum = 0

    for year in years:
        score += row[year] * weights[year]
        weight_sum += weights[year]

    weighted_scores[chapter] = score / weight_sum

# =========================
# ROTATION GROUPS
# =========================
rotation_groups = {
    "Physics": {
        "Mechanics": [
            "Laws of Motion",
            "Work Power Energy",
            "Rotational Motion"
        ],
        "Electricity": [
            "Electrostatics",
            "Current Electricity",
            "Capacitance"
        ],
        "Modern": [
            "Modern Physics",
            "Semiconductors",
            "Nuclear Physics"
        ],
        "Optics": [
            "Ray Optics",
            "Wave Optics"
        ]
    },

    "Chemistry": {
        "Physical": [
            "Thermodynamics",
            "Electrochemistry",
            "Chemical Kinetics"
        ],
        "Organic": [
            "Hydrocarbons",
            "Amines"
        ],
        "Inorganic": [
            "p Block Elements",
            "d and f Block Elements",
            "Coordination Compounds"
        ]
    },

    "Mathematics": {
        "Calculus": [
            "Limits",
            "Continuity and Differentiability",
            "Definite Integration",
            "Application of Derivatives"
        ],
        "Algebra": [
            "Matrices",
            "Determinants",
            "Complex Number"
        ],
        "Coordinate": [
            "Straight Lines",
            "Circle",
            "Parabola"
        ]
    }
}

rotation_boost = {}
latest_year = max(years)

groups = rotation_groups.get(subject, {})

for group, chapters in groups.items():

    existing = chapter_year_counts.index.intersection(chapters)

    if len(existing) == 0:
        continue

    recent_counts = chapter_year_counts.loc[
        existing, latest_year
    ].sum()

    if recent_counts < papers_per_year.get(latest_year, 1):
        for ch in chapters:
            rotation_boost[ch] = ROTATION_BOOST

# =========================
# FINAL SCORES
# =========================
final_scores = {}

for chapter, score in weighted_scores.items():
    boost = rotation_boost.get(chapter, 1.0)
    final_scores[chapter] = score * boost

# =========================
# SCALE TO PAPER SIZE
# =========================
total_score = sum(final_scores.values())

scaled_scores = {
    ch: (score / total_score) * TOTAL_QUESTIONS_PER_PAPER
    for ch, score in final_scores.items()
}

# =========================
# OUTPUT
# =========================
print("\n===== NEXT PAPER PREDICTION =====\n")

sorted_predictions = sorted(
    scaled_scores.items(),
    key=lambda x: x[1],
    reverse=True
)

for chapter, score in sorted_predictions[:15]:
    print(f"{chapter:<35} → {score:.2f} questions")


