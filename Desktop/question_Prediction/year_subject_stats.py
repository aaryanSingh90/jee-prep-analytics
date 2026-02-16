import pandas as pd

# ---------- CONFIG ----------
DATA_PATH = "/Users/aaryansingh/Desktop/question_Prediction/output/finalDataSheet/predicted_questions.csv"

# ---------- LOAD ----------
df = pd.read_csv(DATA_PATH)

# remove bad rows if any
df = df.dropna(subset=["year", "subject"])

df["year"] = df["year"].astype(int)

# ---------- GROUP DATA ----------
stats = df.groupby(["year", "subject"]).size().unstack(fill_value=0)

# ---------- PRINT RESULTS ----------
print("\n===== Year-wise Question Distribution =====\n")

for year in sorted(stats.index):

    print(year)

    year_total = 0

    for subject in stats.columns:
        count = stats.loc[year, subject]
        print(f"{subject:<12}: {count}")
        year_total += count

    print(f"Total       : {year_total}\n")

print("Done.")
