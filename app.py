from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app) # Allows your frontend to talk to this backend

# Replace with your Resend API Key
RESEND_API_KEY = "your_resend_api_key_here"
ADMIN_EMAIL = "your-email@example.com"

# Mock Database
student_data = {
    "fees": "The admission fee for Computer Engineering is ₹1,20,000 per year.",
    "exam": "The Semester VIII exams are scheduled to start from May 15th.",
    "syllabus": "You can download the syllabus from the 'Academics' folder in S3."
}

@app.route('/chat', methods=)
def chat():
    user_msg = request.json.get("message", "").lower()
    
    # Simple logic to find the answer 
    answer = "I'm sorry, I don't have information on that. Try 'fees', 'exam', or 'syllabus'."
    for key in student_data:
        if key in user_msg:
            answer = student_data[key]
            break
            
    return jsonify({"answer": answer})

@app.route('/report', methods=)
def report():
    # Send email notification using Resend API 
    res = requests.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
        json={
            "from": "onboarding@resend.dev",
            "to": ADMIN_EMAIL,
            "subject": "Chatbot Alert: Invalid Answer",
            "html": "<p>A student reported an incorrect answer in the chatbot portal.</p>"
        }
    )
    return jsonify({"status": "Admin Notified!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)