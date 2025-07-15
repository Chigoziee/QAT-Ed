import time, io
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from waitress import serve
from modules.DB import DynamoDBTable
from modules.GPT import OpenAICalls

# Flask app initialization
app = Flask(__name__)
openai = OpenAICalls()
files_db = DynamoDBTable('Files')   # Table to store uploaded file metadata
test_db = DynamoDBTable("Test")     # Table to store test questions and answers

# Enable CORS for all origins
CORS(app, resources={r"/*": {
    "origins": ["*"],
    "allow_headers": ["Content-Type", "Authorization", "API-KEY"],
    "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    "supports_credentials": True
}})


@app.route('/')
def home():
    return "API is live 🌍🌍🌍"


@app.route("/upload", methods=['POST'])
def upload():
    # Extract subject and optional description from form
    subject = request.form.get('subject')
    if not subject:
        return jsonify({'error': "missing required field - subject"}), 400

    description = request.form.get('description', "")
    uploaded_file = request.files.get('file')

    # Convert uploaded file to file-like object
    file_bytes = uploaded_file.read()
    file_like = io.BytesIO(file_bytes)
    file_like.name = uploaded_file.filename

    # Upload file to OpenAI and save metadata to DB
    if uploaded_file:
        uploader = openai.upload(file_like)
        upload_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if uploader:
            upload_data = {
                "Description": {"S": description},
                "UploadedAt": {"S": upload_time},
                "Subject": {"S": subject.title()},
                "file_id": {"S": uploader}
            }
            files_db.write(upload_data)
            return jsonify(upload_data)
        else:
            return jsonify({'error': "upload failed"}), 500
    else:
        return jsonify({'error': "missing required field - file"}), 400


@app.route("/query", methods=['POST'])
def ask():
    # Extract subject and question from request
    subject  = request.json.get("subject")
    question = request.json.get("question")

    if not subject or not question:
        return jsonify({"error": "missing required field"}), 400

    # Retrieve uploaded file_id by subject
    file_id = files_db.read({'Subject': {'S': subject.title()}})["file_id"]["S"]

    # Query OpenAI and parse structured response
    raw = openai.query(file_id, question)
    parts = raw.split("\n\n")  # Expected 5 parts
    resp_dict = {
        "answer":          parts[0],
        "bullet_points":   parts[1].split('\n'),
        "test_question":   parts[2],
        "test_question_id": parts[3],
    }

    # Send response to user
    response = make_response(jsonify(resp_dict), 200)

    # Log test data after response is sent
    @response.call_on_close
    def save_test():
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item = {
            "createdAt": {"S": created_at},
            "question":  {"S": parts[2]},
            "answer":    {"S": parts[4]},
            "Test_id":   {"S": parts[3]},
        }
        test_db.write(item)

    return response


@app.route('/evaluate', methods=['POST'])
def assessment():
    # Extract test_id and user answer
    test_id = request.json.get("test_id")
    answer = request.json.get("answer")

    if not answer or not test_id:
        return jsonify({"error": "missing required field"}), 400

    # Retrieve correct test answer from DB
    test_data = test_db.read({'Test_id': {'S': test_id}})
    if test_data is None:
        return jsonify({"error": "incorrect test id"}), 400

    # Construct input for evaluation call
    query = f'''test_question: {test_data["question"]["S"]},
                test_answer: {test_data["answer"]["S"]},
                user_answer: {answer}'''

    # Get result from OpenAI evaluation
    raw = openai.evaluate(query)
    parts = raw.split('\n')
    result = {
        "knowledge_understood": parts[0],
        "knowledge_confidence": parts[1]
    }
    return jsonify(result)


if __name__ == "__main__":
    # Use waitress to serve Flask app
    serve(app, host="0.0.0.0", port=5006)