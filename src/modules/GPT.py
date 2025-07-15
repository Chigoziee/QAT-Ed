from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


class OpenAICalls:
    def __init__(self):
        self.client = OpenAI()

    def upload(self, file):
            file = self.client.files.create(file=file, purpose="user_data")
            return file.id

    def query(self, file_id: str, question: str):
        response = self.client.responses.create(
            model="gpt-4o-2024-05-13",
            input=[{"role": "user",
                    "content": [{"type": "input_file", "file_id": file_id, },
                                {"type": "input_text", "text": question, }, ]},
                   {"role": "system",
                    "content": """You are a Q.A.T (Question, Answer & Test) assistant. For every user question, 
                    return you answer in 5 paragraphs: 1) a clear answer, 2) 3-5 bullet points summarizing the key information, 3) a follow-up 
                    test question within the scope of the provided document to evaluate understanding, 4) a random 
                    6 digit alphanumeric string, and 5) an answer to the test question. do not add any headers or formating 
                    to the paragraghs just the solution/answers"""
                    }])
        return response.output_text

    def evaluate(self, test: str):
        response = self.client.responses.create(
            model="gpt-4o-2024-05-13",
            input=[{"role": "user",
                    "content": test,},
                   {"role": "system",
                    "content": """You are a Q.A (Question, Answer) evaluator. you will be provided with a test question,
                    with it's solution and then a user's answer to the test question. your job is to evaluate if 
                    the student understands the test question based on their answer to the test question respond in only 
                    two paragaraphs: 1) a bool value indicating that the user understood the answer provided True if the 
                    user understood the answer, False if the user did not understand the answer. 2) an integer value 
                    (in %) indicating how confident the evaluation is e.g. 70, 85. your response should be in this format
                    False\n55"""}])
        return response.output_text


# gpt = OpenAICalls()
# # print(gpt.upload(open("2f874050-d102-44be-a5d6-d480f9dc074d-Organic Chemistry.pdf", "rb")))
# file_id = "file-YWy6v4WmfUtznLxHMchReb"
# question = ("what are functional groups?")
# # #
# print(gpt.query("file-YWy6v4WmfUtznLxHMchReb", question))
# test = '''test_question: "Name the functional group present in the following compounds: (a) CH3CH2OH (b) CH3COOH (c) CH3CH2NH2"
#           test_answer: "(a) Hydroxyl group (-OH) (b) Carboxyl group (-COOH) (c) Amino group (-NH2)"
#           user_answer: Hydroxyl group, Carboxyl group, Amino group'''
#
# print(gpt.evaluate(file_id, test))
