from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Initialize OpenAI client globally
client = OpenAI()


class OpenAICalls:
    def __init__(self):
        # Create a new instance of the OpenAI client
        self.client = OpenAI()

    def upload(self, file):
        """
        Upload a file to OpenAI to be used for context in completions.

        Parameters:
        file: A file-like object to upload.

        Returns:
        str: The ID of the uploaded file.
        """
        file = self.client.files.create(file=file, purpose="user_data")
        return file.id

    def query(self, file_id: str, question: str):
        """
        Ask a question based on the uploaded file and receive a Q.A.T response.

        Parameters:
        file_id (str): ID of the file uploaded to OpenAI.
        question (str): The user question.

        Returns:
        str: Raw multi-part response text from OpenAI.
        """
        response = self.client.responses.create(
            model="gpt-4o-2024-05-13",
            input=[
                {"role": "user",
                 "content": [
                     {"type": "input_file", "file_id": file_id},
                     {"type": "input_text", "text": question}
                 ]},
                {"role": "system",
                 "content": """You are a Q.A.T (Question, Answer & Test) assistant. For every user question, 
                    return your answer in 5 paragraphs: 1) a clear answer, 2) 3-5 bullet points summarizing the key information, 
                    3) a follow-up test question within the scope of the provided document to evaluate understanding, 
                    4) a random 6-digit alphanumeric string, and 5) an answer to the test question. 
                    Do not add any headers or formatting to the paragraphs—just the raw solution."""
                 }
            ])
        return response.output_text

    def evaluate(self, test: str):
        """
        Evaluate a user's answer to a test question based on a reference answer.

        Parameters:
        test (str): A string containing the test question, the correct answer, and the user's answer.

        Returns:
        str: Two-line response with a boolean and a confidence score (e.g., "True\n85").
        """
        response = self.client.responses.create(
            model="gpt-4o-2024-05-13",
            input=[
                {"role": "user", "content": test},
                {"role": "system",
                 "content": """You are a Q.A (Question, Answer) evaluator. You will be provided with a test question,
                    its solution, and a user's answer. Your job is to evaluate if 
                    the student understands the test question based on their answer. Respond in only 
                    two paragraphs: 1) a bool value indicating whether the user understood the answer (True/False), 
                    and 2) an integer (in %) indicating your confidence (e.g., 70, 85). Format: False\n55"""
                 }
            ])
        return response.output_text
