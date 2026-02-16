import pandas as pd

# =========================
# CONFIG
# =========================
DATA_PATH = "/Users/aaryansingh/Desktop/question_Prediction/output/finalDataSheet/predicted_questions.csv"
TOTAL_QUESTIONS_PER_PAPER = 25
ROTATION_BOOST = 1.05
DEFAULT_DIFFICULTY = 1.6

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

df = df.dropna(subset=["year", "subject", "unit_name"])
df["year"] = df["year"].astype(int)

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
    print("No data found.")
    exit()

# =========================
# PAPER COUNT
# =========================
df["paper_id"] = df["year"].astype(str) + "_" + df["exam_session"].astype(str)
papers_per_year = df.groupby("year")["paper_id"].nunique()

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
# RECENCY WEIGHTING
# =========================
years = sorted(chapter_freq.columns)
weights = {year: i + 1 for i, year in enumerate(years)}

weighted_scores = {}

for chapter, row in chapter_freq.iterrows():
    weighted_scores[chapter] = (
        sum(row[y] * weights[y] for y in years)
        / sum(weights.values())
    )

# =========================
# ROTATION BOOST
# =========================
rotation_groups = {
    "Physics": {
        "Mechanics": ["Laws of Motion","Work Power Energy","Rotational Motion"],
        "Electric": ["Electrostatics","Current Electricity"],
        "Optics": ["Ray Optics","Wave Optics"]
    }
}

rotation_boost = {}
latest_year = max(years)

for group, chapters in rotation_groups.get(subject, {}).items():
    existing = chapter_year_counts.index.intersection(chapters)

    if len(existing) == 0:
        continue

    recent_counts = chapter_year_counts.loc[
        existing, latest_year
    ].sum()

    if recent_counts < papers_per_year.get(latest_year, 1):
        for ch in chapters:
            rotation_boost[ch] = ROTATION_BOOST

# Apply rotation boost
final_scores = {}

for chapter, score in weighted_scores.items():
    boost = rotation_boost.get(chapter, 1.0)
    final_scores[chapter] = score * boost

# =========================
# SCALE TO REAL PAPER SIZE
# =========================
total_score = sum(final_scores.values())

scaled_scores = {
    ch: (score / total_score) * TOTAL_QUESTIONS_PER_PAPER
    for ch, score in final_scores.items()
}

# =========================
# UNIT WEIGHTAGE BOOST / PENALTY
# =========================
# Positive boost = more weight
# Negative (<1) = reduce weight

unit_adjustment = {

    "Mathematics": {
        "Calculus": {
            "chapters": [
                "Limits","Continuity and Differentiability",
                "Definite Integration","Application of Derivatives",
                "Differential Equations","Area Under Curves"
            ],
            "factor": 1.20
        },
        "Algebra": {
            "chapters": [
                "Complex Number","Quadratic Equation",
                "Matrices","Determinants",
                "Permutation Combination",
                "Binomial Theorem","Sequences and Series"
            ],
            "factor": 1.15
        },
        "Low Priority": {
            "chapters": ["Trigonometric Equations"],
            "factor": 0.90
        }
    },

    "Physics": {
        "Mechanics": {
            "chapters": [
                "Laws of Motion","Work Power Energy",
                "Rotational Motion","Gravitation"
            ],
            "factor": 1.20
        },
        "Electromagnetism": {
            "chapters": [
                "Electrostatics","Current Electricity",
                "Magnetic Effects of Current"
            ],
            "factor": 1.18
        },
        "Modern Physics": {
            "chapters": [
                "Semiconductors","Modern Physics"
            ],
            "factor": 1.15
        }
    },

    "Chemistry": {
        "GOC": {
            "chapters": ["General Organic Chemistry"],
            "factor": 1.20
        },
        "Physical": {
            "chapters": [
                "Thermodynamics",
                "Chemical Kinetics",
                "Electrochemistry"
            ],
            "factor": 1.15
        },
        "Inorganic": {
            "chapters": [
                "Coordination Compounds",
                "p Block Elements"
            ],
            "factor": 1.12
        }
    }
}

for unit, info in unit_adjustment.get(subject, {}).items():
    for ch in info["chapters"]:
        if ch in scaled_scores:
            scaled_scores[ch] *= info["factor"]

# Re-normalize after boosts
total_score = sum(scaled_scores.values())

scaled_scores = {
    ch: (score / total_score) * TOTAL_QUESTIONS_PER_PAPER
    for ch, score in scaled_scores.items()
}

# =========================
# FINAL PREDICTION OUTPUT
# =========================
print("\n===== NEXT PAPER PREDICTION =====\n")

sorted_predictions = sorted(
    scaled_scores.items(),
    key=lambda x: x[1],
    reverse=True
)

for chapter, score in sorted_predictions[:15]:
    print(f"{chapter:<35} → {score:.2f} questions")

# =========================
# RANK BOOSTER FINDER
# =========================
print("\n===== RANK BOOSTER TOPICS =====\n")

difficulty_map = {
    "Mathematics": {
        "Three Dimensional Geometry": 1.0,
        "Vector Algebra": 1.0,
        "Matrices": 1.0,
        "Determinants": 1.0
    },
    "Physics": {
        "Semiconductors": 1.0,
        "Units and Dimensions": 1.0
    },
    "Chemistry": {
        "Chemical Kinetics": 1.1,
        "Solutions": 1.1
    }
}

rank_scores = {}

for chapter, questions in scaled_scores.items():
    diff = difficulty_map.get(subject, {}).get(
        chapter, DEFAULT_DIFFICULTY
    )
    rank_scores[chapter] = questions / diff

rank_sorted = sorted(
    rank_scores.items(),
    key=lambda x: x[1],
    reverse=True
)

for chapter, score in rank_sorted[:12]:
    print(f"{chapter:<35} → Booster Score: {score:.2f}")
