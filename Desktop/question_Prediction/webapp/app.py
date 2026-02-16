# from flask import Flask, render_template, jsonify
# import pandas as pd
# import os

# app = Flask(__name__)

# @app.route("/")
# def dashboard():
#     return render_template("dashboard.html")

# # API: Get predictions
# @app.route("/api/predictions")
# def predictions():
#     path = "../output/finalDataSheet/predicted_questions.csv"

#     if not os.path.exists(path):
#         return jsonify([])

#     df = pd.read_csv(path)

#     # LIMIT rows for table
#     df = df.head(200)

#     data = df.to_dict(orient="records")
#     return jsonify(data)

# @app.route("/api/chart-data")
# def chart_data():
#     path = "../output/finalDataSheet/predicted_questions.csv"

#     if not os.path.exists(path):
#         return jsonify({})

#     df = pd.read_csv(path)

#     # Example aggregation
#     subject_counts = df["Subject"].value_counts().to_dict()

#     return jsonify(subject_counts)


# # Simulate model run
# import subprocess

# @app.route("/api/predict")
# def simulate_prediction():
#     try:
#         # Run prediction pipeline
#         subprocess.run(
#             ["python", "../predict_dataset.py"],
#             check=True
#         )

#         subprocess.run(
#             ["python", "../Rank_Booster.py"],
#             check=True
#         )

#         return jsonify({"status": "Predictions Updated"})
    
#     except Exception as e:
#         return jsonify({"error": str(e)})


# if __name__ == "__main__":
#     app.run(debug=True)

