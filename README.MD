 # EB-1A RFE Risk Analyzer

VisaCompanion's *EB-1A RFE Risk Analyzer* is a prototype system that reviews draft EB-1A immigration petitions and flags potential weaknesses that could trigger a Request for Evidence (RFE) from USCIS. It simulates a legal-quality assurance assistant that analyzes the petition line-by-line and outputs a detailed report with red flag classifications, severity, and suggestions.

---

## 🚀 Features

- Accepts petition input in .txt, .docx, or .pdf petition drafts
- Segments the document into EB-1A-related sections (e.g., awards, contributions)
- Detects common RFE risk patterns using a mix of:
  - Rule-based string patterns
  - ML classification (trained on denial phrases)
- Maps each red flag to an EB-1A criterion
- Assigns severity ratings (Low / Medium / High)
- Provides improvement suggestions and reviewer notes
- Generates a clean QA Memo in *DOCX* and *PDF* formats

---
## 🧠 EB-1A Criteria Covered

1. Awards
2. Memberships
3. Published Material
4. Judging
5. Original Contributions
6. Authorship
7. Artistic Exhibitions
8. Leading/Critical Roles
9. High Salary
10. Commercial Success

## 📁 Folder Structure


---
EB1A_RFE_Analyzer_Final/
├── analyze_petition.py
├── generate_report.py
├── predict_labels.py
├── training_data.csv
├── model/
│   ├── model.pkl
│   └── vectorizer.pkl
├── red_flag_rules.json
├── petition_analysis/
│   └── (generated JSON outputs)
├── reports/
│   └── (generated reports in DOCX/PDF)
├── sample_petition.txt
├── sample_petition2.txt
├── sample_petition3.txt
├──train_classifier.py
├── requirements.txt
└── README.md

---

## ⚙ Setup Instructions

1. Clone or download the ZIP of this repo
2. Navigate to the folder in terminal
3. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows


## ⚙ How to Run

1. *Install dependencies*  
   ```bash
   pip install -r requirements.txt
   
2.	Run the analyzer on a petition
Edit analyze_petition.py and set: INPUT_FILE = "sample_petition.txt"
Then run: python generate_report.py
3. Generate the QA Memo report
After analysis JSON is saved in petition_analysis/, run: python generate_report.py


📊 Model Training 

To retrain or extend the model:
	1.	Edit or expand training_data.csv with more red flag phrases and EB-1A labels
	2.	Run the model training script train_classifiers.py:
      python train_classifiers.py 
    It will regenerate classifier_model.joblib and tfidf_vectorizer.joblib in the model/ folder


⸻

💡 Red Flag Pattern (Rule-Based) 

{
  "Criterion 1 - Awards": [
    "no evidence of a nationally or internationally recognized award",
    "award is not competitive or merit-based"
  ],
  "Common Denials": [
    "failed to demonstrate",
    "no final merits determination required"
  ]
}



📤 Sample Output

The final QA memo looks like this (DOCX or PDF):
1. 	•	Executive Summary
2. 	•	Table of Contents
3. 	•	Section-by-section Red Flag Analysis
4. 	•	Each issue includes:
5. 	•	Criterion
6. 	•	Matched Phrase
7. 	•	Full Sentence
8. 	•	Severity Rating
9. 	•	Suggested Fix
10. 	•	Reviewer Note
    





📌 Notes
	•	You can drop in any .docx or .pdf petition file by updating INPUT_FILE
	•	Output reports are saved to the reports/ folder with same base filename
	•	Red flags and suggestions are based on real AAO, USCIS Policy Manual, and RFE examples

⸻
  
💡 Future Improvements
	•	Add advanced NLP using spaCy custom NER or transformers
	•	Integrate FAISS/Chroma vector DB for internal phrase search
	•	Include section-by-section word count or document health scores
	•	Build a web UI for lawyers to upload petitions directly

👤 Author

Chigozie Ibekwe Ghislian built for VisaCompanion.ai as a demonstration of practical legal AI tooling.

