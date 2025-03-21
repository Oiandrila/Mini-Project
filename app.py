import os
import google.generativeai as genai
import fitz  # PyMuPDF for PDFs
import docx
from flask import Flask, request, render_template, jsonify

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Signin')
def signin():
    return render_template('Signin.html')

@app.route('/Signup')
def signup():
    return render_template('Signup.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Ensure upload folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Gemini API Key (Replace with your actual API key)
API_KEY = "AIzaSyCSBVAsQvrnFzK0hRdF15RtgmeOzaY7WzU"
genai.configure(api_key=API_KEY)

# Function: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"🔴 Error reading PDF: {str(e)}")
    return text.strip()

# Function: Extract text from DOCX
def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"🔴 Error reading DOCX: {str(e)}")
        return ""

# Function: Generate Interview Questions
def generate_questions(cv_text):
    prompt = (
        f"Based on the following resume, create an interview with technical, "
        f"non-technical, and psychometric questions. "
        f"Return ONLY the questions:\n{cv_text[:2000]}"
    )

    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    try:
        response = model.generate_content(prompt)
        print("🔹 Raw Gemini Response:", response.text)

        questions = [q.strip() for q in response.text.split("\n") if q.strip()]

        # Remove headers like "Interview Questions" if present
        if questions and ("Interview Questions" in questions[0]):
            questions.pop(0)

        return questions if len(questions) >= 5 else questions + ["(Generated question missing)"] * (5 - len(questions))

    except Exception as e:
        print("🔴 Error generating questions:", str(e))
        return ["Error generating questions"]

# Function: Evaluate Responses & Assign Score (Fixed)
def evaluate_answers(answers):
    prompt = (
        "Evaluate the following interview answers and assign a total score out of 100. "
        "Provide constructive feedback and whether the candidate is likely to pass. "
        "DO NOT provide expected answers.\n\nAnswers:\n"
        f"{answers}"
    )

    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    try:
        response = model.generate_content(prompt)
        print("🔹 Gemini Response (Evaluation Only):", response.text)
        return response.text  # Returns evaluation without expected answers
    except Exception as e:
        print("🔴 Error in Gemini API:", str(e))
        return "Error evaluating answers"

# Route: Homepage
@app.route("/")
def index():
    return render_template("index.html")

# Route: Upload Resume
@app.route("/upload", methods=["POST"])
def upload_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    file_ext = file.filename.split(".")[-1].lower()
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    if file_ext == "pdf":
        resume_text = extract_text_from_pdf(file_path)
    elif file_ext == "docx":
        resume_text = extract_text_from_docx(file_path)
    else:
        return jsonify({"error": "Unsupported file format"}), 400

    print("🔹 Extracted Resume Text (First 500 chars):", resume_text[:500])

    questions = generate_questions(resume_text)

    return jsonify({"questions": questions})

# Route: Submit Answers & Get Score
@app.route("/submit_answers", methods=["POST"])
def submit_answers():
    try:
        data = request.get_json()
        print("🔹 Received Data:", data)

        if not data or "answers" not in data:
            return jsonify({"error": "No answers provided"}), 400

        answers = data["answers"]

        if not answers or not isinstance(answers, list):
            return jsonify({"error": "Invalid answers format"}), 400

        formatted_answers = "\n".join(answers)
        print("🔹 Formatted Answers:", formatted_answers)

        score = evaluate_answers(formatted_answers)
        print("🔹 Gemini Response:", score)

        return jsonify({
            "status": "success",
            "score": score,
            "answers": answers
        })

    except Exception as e:
        print("🔴 Error:", str(e))
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)