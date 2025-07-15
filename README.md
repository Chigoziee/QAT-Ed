# Q.A.T (Question, Answer & Test) System

This Flask-based web application is a Q.A.T (Question, Answer & Test) system that allows users to upload research documents, ask questions about the documents, and be tested on their understanding through automatically generated test questions. It uses OpenAI's GPT API for generating content and AWS DynamoDB for persistent storage.

---

## ✨ Features

- Upload research documents (PDF format).
- Ask questions related to the uploaded documents.
- Receive detailed answers, bullet points, and test questions.
- Automatically evaluates the user's understanding of the material.
- Stores uploaded file metadata and generated test questions in DynamoDB.

---

## 🛠 Technologies Used

- **Flask** (Web framework)
- **OpenAI GPT-4o API** (LLM processing)
- **Amazon DynamoDB** (NoSQL Database)
- **Waitress** (Production WSGI server)
- **Python 3.10+**
- **dotenv** (Environment variable loading)

---

## 📦 Project Structure
    QAT-Ed/
    ├── src/
    │ ├── app.py         # Main Flask application
    │ └── modules/
    │   ├── DB.py        # DynamoDB read/write wrapper
    │   └── GPT.py       # OpenAI API interaction
    ├── .env             # Environment variables
    ├── requirements.txt # Python dependencies
    └── README.md        # This documentation

---

## 🚀 Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/Chigoziee/QAT-Ed.git
cd QAT-Ed
```
2. **Create Virtual Environment**
```
 python -m venv .venv
 source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```
3. **Install Dependencies**
```
pip install -r requirements.txt
```
4. **Setup Environment Variables**
   
  Create a .env file in the project root and add your OpenAI and AWS credentials:
```
OPENAI_API_KEY=your-openai-api-key
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

## 🔧 AWS DynamoDB Configuration (Required)
Before running the application, you must create two DynamoDB tables in your AWS account:

1. **Files Table**
   
Primary key: Subject (Type: String)

2. **Test Table**
   
Primary key: Test_id (Type: String)

These tables are used to persist uploaded documents and test questions/answers for later evaluation.

## 🧪 API Endpoints

**✅ /upload – Upload Research Document**

Method: POST

Content-Type: multipart/form-data

Fields:

- subject (required): The subject/topic of the document

- description (optional): Short description

- file (required): PDF or research document

Response: JSON metadata of the uploaded file

**✅ /query – Ask a Question**

Method: POST

Content-Type: application/json
```json
{
  "subject": "Chemistry",
  "question": "What are functional groups?"
}
```
Response:
```json
{
  "answer": "Functional groups are...",
  "bullet_points": [ "...", "...", "..." ],
  "test_question": "Name three functional groups...",
  "test_question_id": "ABC123"
}
```

**✅ /evaluate – Evaluate User Answer**

Method: POST

Content-Type: application/json
```json
{
  "test_id": "ABC123",
  "answer": "Hydroxyl, Carboxyl, Amino"
}
```
Response:
```json
{
  "knowledge_understood": true,
  "knowledge_confidence": 87
}
```
## ▶️ Run the App
```bash
python src/app.py
```
Or via Waitress:
```bash
waitress-serve --host=0.0.0.0 --port=5006 src.app:app
```
## 📑 Postman Documentation
https://documenter.getpostman.com/view/33819055/2sB34hH1X9

## ✅ Notes
- Ensure AWS credentials and OpenAI API key are valid.
- You can inspect saved data in DynamoDB under the Files and Test tables.
