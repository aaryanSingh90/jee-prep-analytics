import pandas as pd

DATA_PATH = "/Users/aaryansingh/Desktop/question_Prediction/output/finalDataSheet/predicted_questions.csv"

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# ---------- CLEAN ----------
df = df.dropna(subset=["year", "unit_name", "subject"])

df["year"] = df["year"].astype(int)

years_available = sorted(df["year"].unique())

print("\nAvailable years:", years_available)

# ---------- USER INPUT ----------
subject = input("\nEnter subject (Mathematics/Physics/Chemistry): ")

start_year = int(input("Start year: "))
end_year = int(input("End year: "))

years = list(range(start_year, end_year + 1))

print("\nComputing trends...\n")

sub_df = df[df["subject"] == subject]

trend = (
    sub_df
    .groupby(["unit_name", "year"])
    .size()
    .unstack(fill_value=0)
)

trend = trend.reindex(columns=years, fill_value=0)

# ---------- PRINT TREND ----------
for unit, row in trend.iterrows():

    counts = [str(row[y]) for y in years]

    print(f"{unit}: " + " → ".join(counts))
