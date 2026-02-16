# import streamlit as st
# import pandas as pd
# import joblib
# from pathlib import Path
# from sklearn.metrics.pairwise import cosine_similarity

# # --------------------------------------------------
# # PAGE CONFIG
# # --------------------------------------------------
# st.set_page_config(
#     page_title="Question Prediction Dashboard",
#     layout="wide"
# )

# st.title("📊 JEE Question Prediction Dashboard")

# # --------------------------------------------------
# # PATHS
# # --------------------------------------------------
# DATA_PATH = Path("output/finalDataSheet/predicted_questions.csv")
# VECTORIZER_PATH = Path("recommender_vectorizer.pkl")
# VECTOR_PATH = Path("question_vectors.pkl")

# # --------------------------------------------------
# # LOAD DATASET
# # --------------------------------------------------
# @st.cache_data
# def load_data():
#     if DATA_PATH.exists():
#         df = pd.read_csv(DATA_PATH)

#         # convert string dtype to normal string
#         for col in df.columns:
#             if df[col].dtype.name == "string":
#                 df[col] = df[col].astype(str)

#         return df
#     return None

# df = load_data()

# # --------------------------------------------------
# # SIDEBAR FILTERS
# # --------------------------------------------------
# st.sidebar.header("Filters")

# filtered_df = df.copy() if df is not None else None

# if filtered_df is not None:

#     if "Subject" in filtered_df.columns:
#         subject = st.sidebar.selectbox(
#             "Subject",
#             ["All"] + sorted(filtered_df["Subject"].dropna().unique())
#         )

#         if subject != "All":
#             filtered_df = filtered_df[filtered_df["Subject"] == subject]

#     if "Chapter" in filtered_df.columns:
#         chapter = st.sidebar.selectbox(
#             "Chapter",
#             ["All"] + sorted(filtered_df["Chapter"].dropna().unique())
#         )

#         if chapter != "All":
#             filtered_df = filtered_df[filtered_df["Chapter"] == chapter]

# # --------------------------------------------------
# # DASHBOARD
# # --------------------------------------------------
# if filtered_df is not None:

#     col1, col2 = st.columns(2)

#     col1.metric("Total Questions", len(filtered_df))

#     if "Year" in filtered_df.columns:
#         col2.metric("Years Covered", filtered_df["Year"].nunique())

#     st.divider()

#     st.subheader("Predicted Questions")

#     st.dataframe(filtered_df, use_container_width=True)

#     csv = filtered_df.to_csv(index=False).encode("utf-8")

#     st.download_button(
#         "⬇ Download Filtered Data",
#         csv,
#         "filtered_questions.csv",
#         "text/csv",
#     )

# else:
#     st.error("predicted_questions.csv not found!")

# # --------------------------------------------------
# # LOAD RECOMMENDER
# # --------------------------------------------------
# st.divider()
# st.header("🔍 Similar PYQ Finder")

# @st.cache_resource
# def load_recommender():
#     if VECTORIZER_PATH.exists() and VECTOR_PATH.exists():
#         vectorizer = joblib.load(VECTORIZER_PATH)
#         question_vectors = joblib.load(VECTOR_PATH)
#         return vectorizer, question_vectors
#     return None, None

# vectorizer, question_vectors = load_recommender()

# user_question = st.text_area(
#     "Enter a question",
#     height=120
# )

# top_k = st.slider("Number of similar questions", 1, 10, 5)

# if st.button("Find Similar Questions"):

#     if not user_question.strip():
#         st.warning("Please enter a question.")

#     elif vectorizer is None:
#         st.error("Run build_recommender.py first.")

#     else:
#         # Convert question to vector
#         query_vec = vectorizer.transform([user_question])

#         # Compute similarity
#         similarity_scores = cosine_similarity(
#             query_vec,
#             question_vectors
#         )[0]

#         # Top results
#         top_indices = similarity_scores.argsort()[-top_k:][::-1]

#         # Fetch rows
#         results = df.iloc[top_indices].copy()
#         results["similarity"] = similarity_scores[top_indices]

#         st.subheader("Top Similar Questions")

#         for _, row in results.iterrows():

#             st.markdown("---")

#             year_value = (
#                 row.get("Year")
#                 or row.get("year")
#                 or row.get("Exam")
#                 or row.get("Session")
#                 or "N/A"
#             )

#             st.markdown(f"### 📅 Year: {year_value}")

#             st.markdown(
#                 f"**Similarity Score:** {row['similarity']:.3f}"
#             )

#             st.markdown("**Question:**")
#             st.write(row.get("question", "Not available"))




# st.divider()
# st.header("📈 Next Paper Chapter Prediction")

# TOTAL_QUESTIONS_PER_PAPER = 25
# ROTATION_BOOST = 1.05

# if df is not None:

#     # Normalize columns for safety
#     data = df.copy()

#     # Rename columns if needed
#     rename_map = {
#         "Year": "year",
#         "Subject": "subject",
#         "Chapter": "unit_name"
#     }

#     for k, v in rename_map.items():
#         if k in data.columns:
#             data.rename(columns={k: v}, inplace=True)

#     required_cols = {"year", "subject", "unit_name"}

#     if required_cols.issubset(data.columns):

#         data = data.dropna(subset=["year", "subject", "unit_name"])
#         data["year"] = data["year"].astype(str).str[:4].astype(int)

#         # Normalize chapter names
#         name_map = {
#             "Dual Nature": "Modern Physics",
#             "Atoms": "Modern Physics",
#             "Nuclei": "Nuclear Physics"
#         }

#         data["unit_name"] = data["unit_name"].replace(name_map)

#         col1, col2 = st.columns(2)

#         with col1:
#             start_year = st.number_input(
#                 "Start Year",
#                 value=int(data["year"].min())
#             )

#         with col2:
#             end_year = st.number_input(
#                 "End Year",
#                 value=int(data["year"].max())
#             )

#         subject = st.selectbox(
#             "Select Subject",
#             sorted(data["subject"].unique())
#         )

#         if st.button("Predict Next Paper"):

#             filtered = data[
#                 (data["year"] >= start_year)
#                 & (data["year"] <= end_year)
#                 & (data["subject"] == subject)
#             ]

#             if filtered.empty:
#                 st.warning("No data available.")
#             else:

#                 # Unique paper id
#                 if "exam_session" in filtered.columns:
#                     filtered["paper_id"] = (
#                         filtered["year"].astype(str)
#                         + "_" +
#                         filtered["exam_session"].astype(str)
#                     )
#                 else:
#                     filtered["paper_id"] = filtered["year"]

#                 papers_per_year = (
#                     filtered.groupby("year")["paper_id"]
#                     .nunique()
#                 )

#                 chapter_year_counts = (
#                     filtered.groupby(["unit_name", "year"])
#                     .size()
#                     .unstack(fill_value=0)
#                 )

#                 chapter_freq = chapter_year_counts.copy()

#                 for year in chapter_freq.columns:
#                     chapter_freq[year] /= papers_per_year.get(year, 1)

#                 years = sorted(chapter_freq.columns)
#                 weights = {year: i + 1 for i, year in enumerate(years)}

#                 weighted_scores = {}

#                 for chapter, row in chapter_freq.iterrows():
#                     score = 0
#                     weight_sum = 0

#                     for year in years:
#                         score += row[year] * weights[year]
#                         weight_sum += weights[year]

#                     weighted_scores[chapter] = score / weight_sum

#                 latest_year = max(years)

#                 rotation_boost = {}
#                 recent_counts = chapter_year_counts[latest_year]

#                 for chapter, count in recent_counts.items():
#                     if count == 0:
#                         rotation_boost[chapter] = ROTATION_BOOST

#                 final_scores = {}

#                 for chapter, score in weighted_scores.items():
#                     boost = rotation_boost.get(chapter, 1.0)
#                     final_scores[chapter] = score * boost

#                 total_score = sum(final_scores.values())

#                 scaled_scores = {
#                     ch: (score / total_score)
#                     * TOTAL_QUESTIONS_PER_PAPER
#                     for ch, score in final_scores.items()
#                 }

#                 predictions = sorted(
#                     scaled_scores.items(),
#                     key=lambda x: x[1],
#                     reverse=True
#                 )[:15]

#                 st.subheader("Predicted Chapter Distribution")

#                 pred_df = pd.DataFrame(
#                     predictions,
#                     columns=["Chapter", "Expected Questions"]
#                 )

#                 st.dataframe(pred_df, use_container_width=True)


# st.divider()
# st.header("📊 Chapter Trend Analysis")

# st.info(
#     "Each year typically contains **8–12 exam sessions**, "
#     "and each session has **25 questions**, so yearly totals "
#     "represent distribution across multiple papers."
# )


# if df is not None:

#     data = df.copy()

#     # Normalize columns
#     rename_map = {
#         "Year": "year",
#         "Subject": "subject",
#         "Chapter": "unit_name"
#     }

#     for k, v in rename_map.items():
#         if k in data.columns:
#             data.rename(columns={k: v}, inplace=True)

#     required_cols = {"year", "subject", "unit_name"}

#     if required_cols.issubset(data.columns):

#         data = data.dropna(subset=["year", "subject", "unit_name"])
#         data["year"] = data["year"].astype(str).str[:4].astype(int)

#         years_available = sorted(data["year"].unique())

#         col1, col2 = st.columns(2)

#         with col1:
#             trend_subject = st.selectbox(
#                 "Subject",
#                 sorted(data["subject"].unique()),
#                 key="trend_subject"
#             )

#         with col2:
#             start_year_trend = st.number_input(
#                 "Start Year",
#                 value=min(years_available),
#                 key="trend_start"
#             )

#         end_year_trend = st.number_input(
#             "End Year",
#             value=max(years_available),
#             key="trend_end"
#         )

#         if st.button("Compute Trends"):

#             years = list(range(
#                 int(start_year_trend),
#                 int(end_year_trend) + 1
#             ))

#             sub_df = data[data["subject"] == trend_subject]

#             trend = (
#                 sub_df
#                 .groupby(["unit_name", "year"])
#                 .size()
#                 .unstack(fill_value=0)
#             )

#             trend = trend.reindex(columns=years, fill_value=0)

#             st.subheader("Chapter Trend Table")
#             st.dataframe(trend, use_container_width=True)

#             st.subheader("Trend Visualization")
#             st.line_chart(trend.T)
# st.divider()
# st.header("📚 Question Distribution by Year")

# st.info(
#     "Each year usually contains **8–12 exam sessions**, "
#     "and each exam has **25 questions**."
# )

# if df is not None:

#     data = df.copy()

#     # Normalize columns
#     rename_map = {
#         "Year": "year",
#         "Subject": "subject",
#         "Chapter": "unit_name"
#     }

#     for k, v in rename_map.items():
#         if k in data.columns:
#             data.rename(columns={k: v}, inplace=True)

#     required_cols = {"year", "subject"}

#     if required_cols.issubset(data.columns):

#         data = data.dropna(subset=["year", "subject"])
#         data["year"] = data["year"].astype(str).str[:4].astype(int)

#         years_available = sorted(data["year"].unique())

#         col1, col2 = st.columns(2)

#         with col1:
#             dist_start_year = st.number_input(
#                 "Start Year",
#                 value=min(years_available),
#                 key="dist_start"
#             )

#         with col2:
#             dist_end_year = st.number_input(
#                 "End Year",
#                 value=max(years_available),
#                 key="dist_end"
#             )

#         if st.button("Show Distribution"):

#             filtered = data[
#                 (data["year"] >= dist_start_year)
#                 & (data["year"] <= dist_end_year)
#             ]

#             # -----------------------------
#             # YEAR + SUBJECT COUNTS
#             # -----------------------------
#             stats = (
#                 filtered
#                 .groupby(["year", "subject"])
#                 .size()
#                 .unstack(fill_value=0)
#             )

#             stats["Total"] = stats.sum(axis=1)

#             st.subheader("Year-wise Subject Distribution")
#             st.dataframe(stats, use_container_width=True)

#             st.subheader("Trend Chart")
#             st.line_chart(stats)

#             # -----------------------------
#             # UNIT DISTRIBUTION
#             # -----------------------------
#             if "unit_name" in filtered.columns:

#                 st.subheader("Chapter Distribution")

#                 unit_stats = (
#                     filtered
#                     .groupby(["year", "unit_name"])
#                     .size()
#                     .unstack(fill_value=0)
#                 )

#                 st.dataframe(unit_stats, use_container_width=True)
#                 st.divider()
# st.header("🏆 Rank Booster Engine")

# TOTAL_QUESTIONS_PER_PAPER = 25
# ROTATION_BOOST = 1.05
# DEFAULT_DIFFICULTY = 1.6

# if df is not None:

#     data = df.copy()

#     rename_map = {
#         "Year": "year",
#         "Subject": "subject",
#         "Chapter": "unit_name"
#     }

#     for k, v in rename_map.items():
#         if k in data.columns:
#             data.rename(columns={k: v}, inplace=True)

#     required_cols = {"year", "subject", "unit_name"}

#     if required_cols.issubset(data.columns):

#         data = data.dropna(subset=["year", "subject", "unit_name"])
#         data["year"] = data["year"].astype(str).str[:4].astype(int)

#         years_available = sorted(data["year"].unique())

#         col1, col2 = st.columns(2)

#         with col1:
#             rb_start_year = st.number_input(
#                 "Start Year",
#                 value=min(years_available),
#                 key="rb_start"
#             )

#         with col2:
#             rb_end_year = st.number_input(
#                 "End Year",
#                 value=max(years_available),
#                 key="rb_end"
#             )

#         rb_subject = st.selectbox(
#             "Subject",
#             sorted(data["subject"].unique()),
#             key="rb_subject"
#         )

#         if st.button("Run Rank Booster"):

#             filtered = data[
#                 (data["year"] >= rb_start_year)
#                 & (data["year"] <= rb_end_year)
#                 & (data["subject"] == rb_subject)
#             ]

#             if filtered.empty:
#                 st.warning("No data found.")
#             else:

#                 if "exam_session" in filtered.columns:
#                     filtered["paper_id"] = (
#                         filtered["year"].astype(str)
#                         + "_" +
#                         filtered["exam_session"].astype(str)
#                     )
#                 else:
#                     filtered["paper_id"] = filtered["year"]

#                 papers_per_year = (
#                     filtered.groupby("year")["paper_id"]
#                     .nunique()
#                 )

#                 chapter_year_counts = (
#                     filtered.groupby(["unit_name", "year"])
#                     .size()
#                     .unstack(fill_value=0)
#                 )

#                 chapter_freq = chapter_year_counts.copy()

#                 for y in chapter_freq.columns:
#                     chapter_freq[y] /= papers_per_year.get(y, 1)

#                 years = sorted(chapter_freq.columns)
#                 weights = {y: i + 1 for i, y in enumerate(years)}

#                 weighted_scores = {}

#                 for chapter, row in chapter_freq.iterrows():
#                     weighted_scores[chapter] = (
#                         sum(row[y] * weights[y] for y in years)
#                         / sum(weights.values())
#                     )

#                 total_score = sum(weighted_scores.values())

#                 scaled_scores = {
#                     ch: (score / total_score)
#                     * TOTAL_QUESTIONS_PER_PAPER
#                     for ch, score in weighted_scores.items()
#                 }

#                 predictions = sorted(
#                     scaled_scores.items(),
#                     key=lambda x: x[1],
#                     reverse=True
#                 )[:15]

#                 st.subheader("📈 Next Paper Prediction")

#                 pred_df = pd.DataFrame(
#                     predictions,
#                     columns=["Chapter", "Expected Questions"]
#                 )

#                 st.dataframe(pred_df, use_container_width=True)

#                 # -----------------------------
#                 # Rank Booster Finder
#                 # -----------------------------
#                 difficulty_map = {
#                     "Mathematics": {
#                         "Three Dimensional Geometry": 1.0,
#                         "Vector Algebra": 1.0,
#                         "Matrices": 1.0,
#                         "Determinants": 1.0
#                     },
#                     "Physics": {
#                         "Semiconductors": 1.0,
#                         "Units and Dimensions": 1.0
#                     },
#                     "Chemistry": {
#                         "Chemical Kinetics": 1.1,
#                         "Solutions": 1.1
#                     }
#                 }

#                 rank_scores = {}

#                 for chapter, questions in scaled_scores.items():
#                     diff = difficulty_map.get(rb_subject, {}).get(
#                         chapter, DEFAULT_DIFFICULTY
#                     )
#                     rank_scores[chapter] = questions / diff

#                 rank_sorted = sorted(
#                     rank_scores.items(),
#                     key=lambda x: x[1],
#                     reverse=True
#                 )[:12]

#                 st.subheader("🏆 Rank Booster Chapters")

#                 rb_df = pd.DataFrame(
#                     rank_sorted,
#                     columns=["Chapter", "Booster Score"]
#                 )

#                 st.dataframe(rb_df, use_container_width=True)








import streamlit as st
import pandas as pd
import joblib
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------------------------
# PAGE CONFIG & CSS
# --------------------------------------------------
st.set_page_config(
    page_title="JEE Prep Analytics",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for modern look
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------------------------
# PAGE CONFIG & ENHANCED CSS
# --------------------------------------------------
st.set_page_config(
    page_title="JEE Prep Analytics",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS to fix the "White Box" issue in Dark Mode
st.markdown("""
    <style>
    /* Metric Card Styling - Transparent with Border */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.3);
        padding: 15px 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Tab Styling - Remove heavy white background */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        color: inherit;
    }

    .stTabs [aria-selected="true"] {
        background-color: #007bff !important;
        color: white !important;
        border: 1px solid #007bff !important;
    }

    /* Expander and Table Styling */
    div[data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 10px;
    }

    /* Dataframe header adjustment */
    .stDataFrame {
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# DATA & PATHS
# --------------------------------------------------
DATA_PATH = Path("output/finalDataSheet/predicted_questions.csv")
VECTORIZER_PATH = Path("recommender_vectorizer.pkl")
VECTOR_PATH = Path("question_vectors.pkl")

@st.cache_data
def load_data():
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
        df.columns = [c.lower() for c in df.columns]
        
        if 'unit_name' in df.columns and 'chapter' not in df.columns:
            df['chapter'] = df['unit_name']
        
        for col in df.columns:
            if df[col].dtype.name == "string":
                df[col] = df[col].astype(str)
        return df
    return None

@st.cache_resource
def load_recommender():
    if VECTORIZER_PATH.exists() and VECTOR_PATH.exists():
        return joblib.load(VECTORIZER_PATH), joblib.load(VECTOR_PATH)
    return None, None

df = load_data()
vectorizer, question_vectors = load_recommender()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
with st.sidebar:
    st.title("🎯 Study Filters")
    if df is not None:
        sub_list = ["All"] + sorted(df['subject'].dropna().unique().tolist())
        sel_subject = st.selectbox("Select Subject", sub_list)
        
        filtered_df = df.copy()
        if sel_subject != "All":
            filtered_df = filtered_df[filtered_df['subject'] == sel_subject]
            
        chap_list = ["All"] + sorted(filtered_df['chapter'].dropna().unique().tolist())
        sel_chapter = st.selectbox("Select Chapter", chap_list)
        
        if sel_chapter != "All":
            filtered_df = filtered_df[filtered_df['chapter'] == sel_chapter]
    
    st.divider()
    st.caption("v2.0.2 | LNCT AIML Dept")

# --------------------------------------------------
# MAIN UI
# --------------------------------------------------
st.title("📊 JEE Question Prediction Dashboard")

if df is None:
    st.error(f"Error: `{DATA_PATH}` not found.")
    st.stop()

tab_main, tab_predict, tab_sim, tab_trends = st.tabs([
    "📂 Dataset Explorer", "🔮 Rank Booster", "🔍 Similar Questions", "📈 Trend Analysis"
])

# --- TAB 1: DATASET EXPLORER ---
with tab_main:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Questions", len(filtered_df))
    c2.metric("Filtered Chapters", filtered_df['chapter'].nunique())
    # Handling year range for metric
    year_min = filtered_df['year'].min()
    year_max = filtered_df['year'].max()
    c3.metric("Year Span", f"{year_min} - {year_max}")

    st.subheader("Question Data Bank")
    st.dataframe(filtered_df, use_container_width=True, height=500)
    
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Filtered CSV", csv_data, "jee_filtered_data.csv", "text/csv")

# --- TAB 2: RANK BOOSTER ---
with tab_predict:
    st.header("🏆 Rank Booster Engine")
    col_l, col_r = st.columns([1, 2])
    
    with col_l:
        target_sub = st.selectbox("Analyze Subject", sorted(df['subject'].unique()), key="rb_sub_box")
        if st.button("Run Prediction Analytics", use_container_width=True):
            st.session_state.run_rb = True
    
    if st.session_state.get('run_rb'):
        rb_data = df[df['subject'] == target_sub]
        top_chaps = rb_data['chapter'].value_counts().head(12).reset_index()
        top_chaps.columns = ['Chapter', 'Frequency']
        
        with col_r:
            st.subheader(f"High-Weightage Chapters: {target_sub}")
            st.bar_chart(data=top_chaps, x="Chapter", y="Frequency", color="#007bff")

# --- TAB 3: SIMILARITY FINDER ---
with tab_sim:
    st.header("🔍 Semantic Search")
    u_input = st.text_area("Paste Question Text", height=150)
    if st.button("Search Matches", type="primary"):
        if vectorizer and u_input.strip():
            query_vec = vectorizer.transform([u_input])
            sim_scores = cosine_similarity(query_vec, question_vectors)[0]
            top_idx = sim_scores.argsort()[-5:][::-1]
            
            for idx in top_idx:
                row = df.iloc[idx]
                with st.expander(f"Match: {sim_scores[idx]:.1%} | {row['year']} | {row['subject']}"):
                    st.write(row.get('question', 'N/A'))
        else:
            st.warning("Please enter text or check if models are loaded.")

# --- TAB 4: TREND ANALYSIS ---
with tab_trends:
    st.header("📈 Chapter Trends")
    t_sub = st.selectbox("Select Subject", sorted(df['subject'].unique()), key="trend_sel")
    trend_df = df[df['subject'] == t_sub].groupby(['year', 'chapter']).size().unstack(fill_value=0)
    st.line_chart(trend_df)

st.divider()
st.markdown("<center style='color:gray'>JEE Prediction System</center>", unsafe_allow_html=True)
