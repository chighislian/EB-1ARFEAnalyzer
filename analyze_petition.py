import os
import json
import spacy
import docx
import fitz  # PyMuPDF

# === CONFIG ===
INPUT_FILE = "sample_petition3.txt"  # Accepts .txt, .docx, or .pdf
RULES_FILE = "red_flag_rules.json"
OUTPUT_FOLDER = "petition_analysis"

nlp = spacy.load("en_core_web_sm")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === Load red flag rules ===
with open(RULES_FILE, "r", encoding="utf-8") as f:
    red_flag_rules = json.load(f)

# === Section headers ===
SECTION_HEADERS = {
    "personal_background": ["personal background", "biographical sketch"],
    "award": ["award", "prize"],
    "membership": ["membership", "organization"],
    "published": ["publication", "authorship"],
    "judge": ["judge", "panel", "reviewer"],
    "contributions": ["contribution", "innovation"],
    "media": ["media", "press", "newspaper", "coverage"],
    "leading_role": ["leading", "critical role"],
    "salary": ["salary", "remuneration"],
    "commercial_success": ["box office", "commercial success", "sales"],
    "exhibitions": ["exhibition", "showcase", "display"],
    "recommendation": ["recommendation letter", "expert letter", "endorsement"]
}

def detect_section(text):
    for section, keywords in SECTION_HEADERS.items():
        for keyword in keywords:
            if keyword.lower() in text.lower():
                return section
    return "introduction"

def match_red_flag(sentence, red_flag_patterns):
    matched_flags = []
    sent_lower = sentence.lower()
    for criterion, patterns in red_flag_patterns.items():
        for pattern in patterns:
            if pattern.lower() in sent_lower or sent_lower in pattern.lower():
                matched_flags.append({
                    "criterion": criterion,
                    "pattern": pattern,
                    "sentence": sentence.strip()
                })
    return matched_flags

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    elif ext == ".docx":
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == ".pdf":
        doc = fitz.open(file_path)
        return "\n".join([page.get_text() for page in doc])
    else:
        raise ValueError("Unsupported file type. Use .txt, .docx, or .pdf")

def analyze_petition(file_path):
    content = extract_text_from_file(file_path)

    sections = {}
    current_section = "introduction"
    buffer = []

    for line in content.splitlines():
        if detect_section(line) != current_section and detect_section(line) != "introduction":
            if buffer:
                sections[current_section] = "\n".join(buffer)
                buffer = []
            current_section = detect_section(line)
        buffer.append(line)

    if buffer:
        sections[current_section] = "\n".join(buffer)

    result = {
        "filename": os.path.basename(file_path),
        "sections": {}
    }

    for sec_name, sec_text in sections.items():
        doc = nlp(sec_text)
        section_flags = []
        for sent in doc.sents:
            sent_text = sent.text.strip()
            matches = match_red_flag(sent_text, red_flag_rules)
            section_flags.extend(matches)

        if section_flags:
            result["sections"][sec_name] = section_flags

    output_path = os.path.join(
        OUTPUT_FOLDER,
        os.path.basename(file_path).replace(".txt", "_analysis.json").replace(".docx", "_analysis.json").replace(".pdf", "_analysis.json")
    )

    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, indent=2)

    print(f"✅ Analysis saved to: {output_path}")

# === Run ===
if __name__ == "__main__":
    analyze_petition(INPUT_FILE)