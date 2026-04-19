from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# Use environment variables (IMPORTANT for Render)
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

# Mock Database
student_data = {
    "fees": "The admission fee for Computer Engineering is ₹1,20,000 per year.",
    "exam": "The Semester VIII exams are scheduled to start from May 15th.",
    "syllabus": "You can download the syllabus from the 'Academics' folder in S3.",
    "admission": "Admissions start from June.",
    "placement": "Average placement is ₹6 LPA.",
    "hostel": "Hostel available.",
    "contact": "Email: info@college.edu",
    "help": "Ask about fees, exam, syllabus, admission, placement."
}

# ✅ FIXED: methods added
@app.route('/')
def home():
    return "EduAssist Backend Running 🚀"
    
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").lower()

    answer = "I'm sorry, I don't have information on that. Try 'fees', 'exam', or 'syllabus'."
    
    for key in student_data:
        if key in user_msg:
            answer = student_data[key]
            break

    return jsonify({"answer": answer})


# ✅ FIXED: methods added
@app.route('/report', methods=['POST'])
def report():
    try:
        res = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "onboarding@resend.dev",
                "to": ADMIN_EMAIL,
                "subject": "Chatbot Alert: Invalid Answer",
                "html": "<p>A student reported an incorrect answer in the chatbot portal.</p>"
            }
        )

        return jsonify({"status": "Admin Notified!", "resend_status": res.status_code})
    
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})


# Render uses PORT env variable
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
