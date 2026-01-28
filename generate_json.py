import os
import json
import re
import sys

PDF_DIR = "pdfs"
OUTPUT_FILE = "data/documents.json"

documents = []

icon_map = {
    "Mathematics": "📘",
    "English": "📗",
    "Chemistry": "🧪",
    "Basic Mechanical Engineering": "⚙️",
    "Engineering Mechanics": "🏗️",
    "Basic Electronics": "🔌"
}

# ensure pdf dir exists
if not os.path.isdir(PDF_DIR):
    print(f"Error: directory '{PDF_DIR}' not found.", file=sys.stderr)
    sys.exit(1)

for filename in sorted(os.listdir(PDF_DIR)):
    # skip non-files and non-pdfs
    path = os.path.join(PDF_DIR, filename)
    if not os.path.isfile(path):
        continue

    base, ext = os.path.splitext(filename)
    if ext.lower() != ".pdf":
        continue

    name = base  # filename without extension
    lower_name = name.lower()

    # SUBJECT DETECTION
    if "chem" in lower_name:
        subject = "Chemistry"
    elif "mechanical" in lower_name or "bme" in lower_name:
        subject = "Basic Mechanical Engineering"
    elif "mechanics" in lower_name:
        subject = "Engineering Mechanics"
    elif "electronics" in lower_name or "basic-electronics" in lower_name or "beee" in lower_name:
        subject = "Basic Electronics"
    elif "math" in lower_name:
        subject = "Mathematics"
    elif "english" in lower_name:
        subject = "English"
    else:
        subject = "English"   # safe fallback

    semester = "1st Semester"

    year_match = re.search(r"(20\d{2})", name)
    year = year_match.group(1) if year_match else "All"

    # Try to capture course code (case-insensitive)
    code_match = re.search(r"[A-Z]{1,}\d+[A-Z0-9\-]*", name.upper())
    code = code_match.group(0) if code_match else ""

    # create a safe slug for id: lowercase, replace non-alphanum with hyphens
    doc_id = re.sub(r"[^a-z0-9]+", "-", lower_name).strip("-")

    icon = icon_map.get(subject, "📄")

    documents.append({
        "id": doc_id,
        "title": f"{subject} ({code})" if code else subject,
        "subject": subject,
        "semester": semester,
        "year": year,
        "icon": icon,
        "file": filename
    })

os.makedirs(os.path.dirname(OUTPUT_FILE) or ".", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=2, ensure_ascii=False)

print("documents.json generated successfully!")
