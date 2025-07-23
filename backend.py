import os
import json
from google import genai
from dotenv import load_dotenv, dotenv_values 
load_dotenv()
class Exercise():
    def __init__(self, level):
        exercise = generate_exercise(level)
        self.title = exercise['title']
        self.paragraph = exercise['paragraph']
        self.questions = exercise['questions']

    def __str__(self):
        return f"Title: {self.title}\nParagraph: {self.paragraph}\nQuestions: {self.questions}"
def generate_exercise(level):
    print(level)
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", contents= f"You are a Swedish language teacher teaching at {level} level Common European Framework of Reference for Languages (CEFR)"+
    """
    You are an expert in teaching Swedish. You are really careful to not make any mistakes and always double-check your work.
    You are also really comprehensive and thorough in your teaching.
    Your main mission is to generate a Swedish paragraph for students to practice reading comprehension.
    The paragraph should be about 200 words long and should be written in a way that is engaging and interesting for students.
    The paragraph must be a narrative text, descriptive text, expository text, or persuasive text.
    The topics must be diverse, but must be suitable for the level specified.
    The paragraph can be daily lifes, a conversation, a guide, an informational text about an object or a particular commentary of the topic
    Higher levels should have more complex vocabulary and sentence structures and more advanced topics.
    Lower levels should have simpler vocabulary and sentence structures and more basic topics.
    The reading exercise should be suitable for students at the sepcified level of the Common European Framework of Reference for Languages (CEFR).
    The paragraph should include a variety of vocabulary and sentence structures to help students improve their reading and comprehension skills.
    6 questions should be generated based on the paragraph to test the students' understanding.
    The questions should be suitable for students at the specified level of the CEFR.
    The questions should be designed to be answered in Swedish and should cover the main ideas and details of the paragraph.
    The questions should be clear and concise, and should not require any prior knowledge of the topic.
    The questions should be multiple choice with 4 options each.
    The questions should be numbered from 1 to 6.
    Your response must be in JSON format with the following structure:
    "{
        "title": "The generated Swedish title",
        "paragraph": "The generated Swedish paragraph",
        "questions": [
            {
                "question": "The question text",
                "options": [
                    "Option A",
                    "Option B",
                    "Option C",
                    "Option D"
                ],
                "answer": "The correct answer option (A, B, C, or D)"
            },
            ...
        ]
    }"
    Make sure to include the paragraph and questions in the JSON response.
    Do not include any additional text or explanations outside of the JSON response.
    Only the JSON response should be returned.
    No other text should be included.
    Make sure to use the correct Swedish grammar and spelling.
    Only generate the JSON response without any additional text.
    remove the beginning "json"
    """
    )
    exercise = json.loads(response.text[8:-4])
    return exercise
def save_api_key(api_key):
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    try:
        with open(env_path, 'w') as f:
            f.write(f"GEMINI_API_KEY=\"{api_key}\"\n")
    except Exception as e:
        raise Exception(f"Failed to save API key: {str(e)}")
    load_dotenv()
def main():
    exercise = generate_exercise('A1-A2')
    print(exercise['paragraph'])
    for i in exercise['questions']:
        print(i['question'])
        for j in i['options']:
            print(j)
        while True:
            answer = input("Your answer (A, B, C, or D): ")
            if i['answer'].lower() == answer.lower():
                print("Correct!")
                break
            else:
                print("Incorrect.")
if __name__ == "__main__":
    main()