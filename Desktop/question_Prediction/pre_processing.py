#physics



# import pdfplumber
# import pandas as pd
# import re
# import os

# # Standard list of chapters to ensure clean matching
# KNOWN_CHAPTERS = [
#     "Mathematics in Physics", "Units and Dimensions", "Motion In One Dimension", 
#     "Motion In Two Dimensions", "Laws of Motion", "Work Power Energy", 
#     "Center of Mass Momentum and Collision", "Rotational Motion", "Gravitation", 
#     "Mechanical Properties of Solids", "Mechanical Properties of Fluids", 
#     "Oscillations", "Waves and Sound", "Thermal Properties of Matter", 
#     "Thermodynamics", "Kinetic Theory of Gases", "Electrostatics", 
#     "Capacitance", "Current Electricity", "Magnetic Properties of Matter", 
#     "Magnetic Effects of Current", "Electromagnetic Induction", 
#     "Alternating Current", "Electromagnetic Waves", "Ray Optics", 
#     "Wave Optics", "Dual Nature of Radiation and Matter", "Atoms", 
#     "Nuclei", "Semiconductors", "Experimental Physics"
# ]

# def normalize(text):
#     """Removes spaces/symbols and converts to lowercase for easy matching."""
#     return re.sub(r'[^a-z0-9]', '', text.lower())

# def extract_jee_data(pdf_path, answer_key_page_start):
#     all_questions = []
    
#     # Dictionary to store answers: key = normalized_chapter_name
#     answer_map = {}
    
#     # Pre-fill dictionary to avoid errors
#     for chapter in KNOWN_CHAPTERS:
#         answer_map[normalize(chapter)] = {}

#     csv_q_counter = 1 
    
#     with pdfplumber.open(pdf_path) as pdf:
#         print(f"Opened PDF: {pdf_path}")
        
#         # --- PHASE 1: PROCESS ANSWER KEYS ---
#         print(f"Reading Answer Keys starting from page {answer_key_page_start}...")
#         current_key_chapter_norm = None
        
#         for i in range(answer_key_page_start - 1, len(pdf.pages)):
#             page_text = pdf.pages[i].extract_text()
#             if not page_text: continue
            
#             lines = page_text.split('\n')
#             for line in lines:
#                 # 1. Identify Chapter Header in Answer Key Section
#                 line_norm = normalize(line)
#                 for chapter in KNOWN_CHAPTERS:
#                     if normalize(chapter) in line_norm:
#                         current_key_chapter_norm = normalize(chapter)
#                         break
                
#                 # 2. Extract Answers (Matches "1. (3)" or "1. 3")
#                 if current_key_chapter_norm:
#                     matches = re.findall(r'(?:^|\s)(\d+)\.\s*\(?(\d+)\)?', line)
#                     for q_num, ans in matches:
#                         answer_map[current_key_chapter_norm][q_num] = ans

#         # --- PHASE 2: PROCESS QUESTIONS ---
#         print("Extracting Questions and matching answers...")
#         current_q_chapter_display = "Unknown"
#         current_q_chapter_norm = "unknown"

#         # Iterate through pages UP TO the answer key section
#         for page in pdf.pages[:answer_key_page_start - 1]:
#             text = page.extract_text()
#             if not text: continue

#             # 1. Identify Chapter Header on Question Page
#             # Check the first few lines for a known chapter name
#             header_candidate = " ".join(text.split('\n')[:4]) 
#             header_candidate_norm = normalize(header_candidate)
            
#             for chapter in KNOWN_CHAPTERS:
#                 if normalize(chapter) in header_candidate_norm:
#                     current_q_chapter_display = chapter  # Clean name for CSV
#                     current_q_chapter_norm = normalize(chapter) # Key for lookup
#                     break
            
#             # 2. Extract Questions
#             blocks = re.split(r'Q(\d+)\.', text)
            
#             for i in range(1, len(blocks), 2):
#                 q_num_orig = blocks[i] # e.g., "1"
#                 q_text_raw = blocks[i+1]
                
#                 # Filter out images
#                 if any(w in q_text_raw.lower() for w in ["figure", "graph", "shown below", "[image"]):
#                     continue
                
#                 clean_text = q_text_raw.replace('\n', ' ').strip()
                
#                 # LOOKUP ANSWER: Use the normalized key + question number
#                 correct_ans = "N/A"
#                 if current_q_chapter_norm in answer_map:
#                     correct_ans = answer_map[current_q_chapter_norm].get(q_num_orig, "N/A")
                
#                 # Extract Options
#                 options_list = re.findall(r'\(\d\).*?(?=\(\d\)|$)', clean_text)
#                 options_str = " | ".join(options_list) if options_list else "Numerical Answer"

#                 all_questions.append({
#                     "exam_name": "JEE Main",
#                     "month": "april",
#                     "subject": "Physics",
#                     "unit_name": current_q_chapter_display,
#                     "question_id": csv_q_counter,
#                     "question_text": clean_text,
#                     "options": options_str,
#                     "correct_option": correct_ans,
#                     "question_length": len(clean_text)
#                 })
#                 csv_q_counter += 1

#     return pd.DataFrame(all_questions)

# if __name__ == "__main__":
#     # Update this path if needed
#     FILE_PATH = "/Users/aaryansingh/Desktop/question_Prediction/data/Physics - JEE Main 2025 April Chapter-wise Question Bank - MathonGo.pdf"
#     OUTPUT_DIR = "/Users/aaryansingh/Desktop/question_Prediction/output/per_paper"
    
#     if not os.path.exists(OUTPUT_DIR):
#         os.makedirs(OUTPUT_DIR)

#     try:
#         # Start extracting (Answer Key starts on page 99)
#         df_results = extract_jee_data(FILE_PATH, answer_key_page_start=94)
        
#         output_file = os.path.join(OUTPUT_DIR, "Physics-JEE Main 2025 April Chapter-wise Question Bank.csv")
#         df_results.to_csv(output_file, index=False)
#         print(f"Success! Processed {len(df_results)} questions.")
#         print(f"File saved to: {output_file}")
#     except Exception as e:
#         print(f"Error: {e}")








#chemistry

# import pdfplumber
# import pandas as pd
# import re
# import os

# ANSWER_KEY_START_PAGE = 105

# KNOWN_CHAPTERS = [
#     "Some Basic Concepts of Chemistry",
#     "Structure of Atom",
#     "States of Matter",
#     "Thermodynamics",
#     "Chemical Equilibrium",
#     "Ionic Equilibrium",
#     "Redox Reactions",
#     "Solutions",
#     "Electrochemistry",
#     "Chemical Kinetics",
#     "Classification of Elements and Periodicity in Properties",
#     "Chemical Bonding and Molecular Structure",
#     "p Block Elements",
#     "d and f Block Elements",
#     "Coordination Compounds",
#     "Practical Chemistry",
#     "General Organic Chemistry",
#     "Hydrocarbons",
#     "Haloalkanes and Haloarenes",
#     "Alcohols Phenols and Ethers",
#     "Aldehydes Ketones and Carboxylic Acids",
#     "Amines",
#     "Biomolecules"
# ]

# # ---------------- NORMALIZE ----------------
# def normalize(text):
#     text = text.lower()
#     text = re.sub(r'\(.*?\)', '', text)
#     text = re.sub(r'[^a-z0-9]', '', text)
#     return text

# # ---------------- ANSWER KEY EXTRACTION ----------------
# def extract_answer_keys(pdf):
#     answer_map = {normalize(c): {} for c in KNOWN_CHAPTERS}

#     current_chapter = None

#     for page in pdf.pages[ANSWER_KEY_START_PAGE - 1:]:
#         text = page.extract_text()
#         if not text:
#             continue

#         # Fix spaced digits
#         text = re.sub(r'(?<=\d)\s+(?=\d)', '', text)

#         lines = text.split('\n')

#         for line in lines:
#             norm_line = normalize(line)

#             # Detect chapter header
#             for chapter in KNOWN_CHAPTERS:
#                 chap_norm = normalize(chapter)
#                 if chap_norm in norm_line:
#                     current_chapter = chap_norm
#                     break

#             if not current_chapter:
#                 continue

#             # Capture answer patterns
#             matches = re.findall(r'(\d+)\.\s*\((\d+)\)', line)

#             for q, ans in matches:
#                 answer_map[current_chapter][q] = ans

#     return answer_map


# # ---------------- QUESTION EXTRACTION ----------------
# def extract_questions(pdf, answer_map):

#     questions = []
#     q_counter = 1

#     current_chapter_display = KNOWN_CHAPTERS[0]
#     current_chapter_norm = normalize(current_chapter_display)

#     for page in pdf.pages[:ANSWER_KEY_START_PAGE - 1]:
#         text = page.extract_text()
#         if not text:
#             continue

#         header_area = " ".join(text.split('\n')[:6])
#         header_norm = normalize(header_area)

#         for chap in KNOWN_CHAPTERS:
#             if normalize(chap) in header_norm:
#                 current_chapter_display = chap
#                 current_chapter_norm = normalize(chap)

#         blocks = re.split(r'Q(\d+)\.', text)

#         for i in range(1, len(blocks), 2):
#             q_num = blocks[i]
#             block = " ".join(blocks[i + 1].split())

#             if len(block) < 10:
#                 continue

#             options = re.findall(r'\(\d\).*?(?=\(\d\)|$)', block)
#             options_str = " | ".join(options) if options else "Numerical Answer"

#             question_text = re.sub(r'\(\d\).*?(?=\(\d\)|$)', '', block)

#             correct_ans = answer_map \
#                 .get(current_chapter_norm, {}) \
#                 .get(q_num, "N/A")

#             questions.append({
#                 "exam_name": "JEE Main",
#                 "month": "January",
#                 "subject": "Chemistry",
#                 "unit_name": current_chapter_display,
#                 "question_id": q_counter,
#                 "question_text": question_text.strip(),
#                 "options": options_str,
#                 "correct_option": correct_ans,
#                 "question_length": len(question_text)
#             })

#             q_counter += 1

#     return pd.DataFrame(questions)


# # ---------------- MAIN ----------------
# def main(pdf_path, output_path):
#     with pdfplumber.open(pdf_path) as pdf:
#         print("Extracting answers...")
#         answer_map = extract_answer_keys(pdf)

#         print("Extracting questions...")
#         df = extract_questions(pdf, answer_map)

#         df.to_csv(output_path, index=False)
#         print("Saved:", output_path)
#         print("Total questions:", len(df))


# # ---------------- RUN ----------------
# if __name__ == "__main__":
#     FILE_PATH = "/Users/aaryansingh/Desktop/question_Prediction/data/Chemistry - JEE Main 2025 April Chapter-wise Question Bank - MathonGo.pdf"
#     OUTPUT_FILE = "/Users/aaryansingh/Desktop/question_Prediction/output/per_paper/JEE Main 2025 April Chapter-wise Question Bank.csv"

#     main(FILE_PATH, OUTPUT_FILE)








#math

# import pdfplumber
# import pandas as pd
# import re
# import os

# # ---------------- CONFIG ----------------
# PDF_PATH = "/Users/aaryansingh/Desktop/question_Prediction/data/Mathematics - JEE Main 2025 April Chapter-wise Question Bank - MathonGo.pdf"
# OUTPUT_CSV = "/Users/aaryansingh/Desktop/question_Prediction/output/per_paper/Math - JEE Main 2025 April Chapter-wise Question Bank.csv"

# # Adjust if answer keys start elsewhere
# ANSWER_KEY_START_PAGE = 64

# KNOWN_CHAPTERS = [
#     "Basic of Mathematics",
#     "Quadratic Equation",
#     "Complex Number",
#     "Sequences and Series",
#     "Permutation Combination",
#     "Binomial Theorem",
#     "Statistics",
#     "Matrices",
#     "Determinants",
#     "Probability",
#     "Sets and Relations",
#     "Functions",
#     "Limits",
#     "Continuity and Differentiability",
#     "Application of Derivatives",
#     "Indefinite Integration",
#     "Definite Integration",
#     "Area Under Curves",
#     "Differential Equations",
#     "Straight Lines",
#     "Circle",
#     "Parabola",
#     "Ellipse",
#     "Hyperbola",
#     "Trigonometric Ratios & Identities",
#     "Trigonometric Equations",
#     "Inverse Trigonometric Functions",
#     "Vector Algebra",
#     "Three Dimensional Geometry"
# ]

# # ---------------- UTILITIES ----------------
# def normalize(text):
#     text = text.lower()
#     text = re.sub(r'\(.*?\)', '', text)
#     text = re.sub(r'[^a-z0-9]', '', text)
#     return text

# def fix_digits(text):
#     # fix spaced numbers
#     text = re.sub(r'(?<=\d)\s+(?=\d)', '', text)
#     return text

# def clean_spaces(text):
#     return " ".join(text.split())


# # ---------------- ANSWER EXTRACTION ----------------
# def extract_answer_keys(pdf):

#     answer_map = {normalize(c): {} for c in KNOWN_CHAPTERS}
#     current_chapter = None

#     for page in pdf.pages[ANSWER_KEY_START_PAGE - 1:]:
#         text = page.extract_text()
#         if not text:
#             continue

#         text = fix_digits(text)
#         lines = text.split('\n')

#         for line in lines:
#             norm_line = normalize(line)

#             # detect chapter
#             for chap in KNOWN_CHAPTERS:
#                 chap_norm = normalize(chap)
#                 if chap_norm in norm_line:
#                     current_chapter = chap_norm
#                     break

#             if not current_chapter:
#                 continue

#             matches = re.findall(r'(\d+)\.\s*\((\d+)\)', line)

#             for q, ans in matches:
#                 answer_map[current_chapter][q] = ans

#     return answer_map


# # ---------------- QUESTION EXTRACTION ----------------
# def extract_questions(pdf, answer_map):

#     all_questions = []
#     q_counter = 1

#     current_chapter_display = KNOWN_CHAPTERS[0]
#     current_chapter_norm = normalize(current_chapter_display)

#     for page in pdf.pages[:ANSWER_KEY_START_PAGE - 1]:

#         text = page.extract_text()
#         if not text:
#             continue

#         header = " ".join(text.split('\n')[:6])
#         header_norm = normalize(header)

#         for chap in KNOWN_CHAPTERS:
#             chap_norm = normalize(chap)
#             if chap_norm in header_norm:
#                 current_chapter_display = chap
#                 current_chapter_norm = chap_norm

#         blocks = re.split(r'Q(\d+)\.', text)

#         for i in range(1, len(blocks), 2):

#             q_num = blocks[i]
#             block = clean_spaces(blocks[i + 1])

#             if len(block) < 10:
#                 continue

#             options = re.findall(r'\(\d\).*?(?=\(\d\)|$)', block)

#             options_str = (
#                 " | ".join(options)
#                 if options else "Numerical Answer"
#             )

#             question_text = re.sub(
#                 r'\(\d\).*?(?=\(\d\)|$)', '',
#                 block
#             ).strip()

#             correct_ans = answer_map \
#                 .get(current_chapter_norm, {}) \
#                 .get(q_num, "N/A")

#             all_questions.append({
#                 "exam_name": "JEE Main",
#                 "month": "april",
#                 "subject": "Mathematics",
#                 "unit_name": current_chapter_display,
#                 "question_id": q_counter,
#                 "question_text": question_text,
#                 "options": options_str,
#                 "correct_option": correct_ans,
#                 "question_length": len(question_text)
#             })

#             q_counter += 1

#     return pd.DataFrame(all_questions)


# # ---------------- MAIN ----------------
# def main():

#     with pdfplumber.open(PDF_PATH) as pdf:

#         print("Reading answer keys...")
#         answer_map = extract_answer_keys(pdf)

#         print("Extracting questions...")
#         df = extract_questions(pdf, answer_map)

#         df.to_csv(OUTPUT_CSV, index=False)

#         print("Saved:", OUTPUT_CSV)
#         print("Total Questions:", len(df))


# if __name__ == "__main__":
#     main()




#combine all the file


import pandas as pd
import os
import glob

# -------- CONFIG --------
INPUT_FOLDER = "/Users/aaryansingh/Desktop/question_Prediction/output/per_paper"
OUTPUT_FOLDER = "/Users/aaryansingh/Desktop/question_Prediction/output/combined"
OUTPUT_FILE = "jee_combined_all_sessions2025.csv"

# -------- CREATE OUTPUT FOLDER --------
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -------- LOAD ALL CSV FILES --------
# This loads all CSV files inside the output folder
csv_files = glob.glob(os.path.join(INPUT_FOLDER, "*.csv"))

if len(csv_files) == 0:
    raise Exception("No CSV files found in input folder.")

print("Files found:")
for f in csv_files:
    print("-", os.path.basename(f))

# -------- READ & MERGE --------
df_list = []

for file in csv_files:
    df = pd.read_csv(file)
    df_list.append(df)

combined_df = pd.concat(df_list, ignore_index=True)

print("Total rows before cleaning:", len(combined_df))

# -------- REMOVE BAD OPTION ROWS --------
combined_df = combined_df[
    combined_df["options"].notna() &
    (combined_df["options"] != "N/A") &
    (combined_df["options"] != "")
]

print("Rows after removing N/A options:", len(combined_df))

# -------- RESET QUESTION ID --------
combined_df = combined_df.reset_index(drop=True)
combined_df["question_id"] = combined_df.index + 1

# -------- SAVE FILE --------
output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
combined_df.to_csv(output_path, index=False)

print("\n✅ Combined dataset saved:")
print(output_path)
print("Final question count:", len(combined_df))
 