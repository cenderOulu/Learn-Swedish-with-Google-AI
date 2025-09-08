import os
import random
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
def paragraph_instructions(level):
    reading_topics = {
    "A1": [
        "A short text about a trip to a supermarket to buy groceries.",
        "A conversation between two people making plans to meet for coffee.",
        "A description of a person's family and home.",
        "A simple set of instructions on how to use a coffee machine or a similar household appliance.",
        "A blog post about a person's favorite hobby, such as reading or playing the guitar.",
        "A short story about losing and finding a wallet."
        "A description of a recent birthday party or a holiday celebration.",
        "A short email to a friend describing a weekend trip to a nearby city.",
        "A recipe for a simple Swedish dish with instructions.",
        "A review of a movie or a restaurant that the person recently visited.",
        "A brief account of a day at work or school, including simple problems and solutions.",
        "A short text about a favorite place to visit and why they like it."
    ],
    "A2": [
        "A description of a recent birthday party or a holiday celebration.",
        "A short email to a friend describing a weekend trip to a nearby city.",
        "A recipe for a simple Swedish dish with instructions.",
        "A review of a movie or a restaurant that the person recently visited.",
        "A brief account of a day at work or school, including simple problems and solutions.",
        "A short text about a favorite place to visit and why they like it."
    ],
    "B1": [
        "An article about a cultural festival or a historical event in Sweden.",
        "A personal letter discussing future plans, such as moving to a new apartment or starting a new job.",
        "A discussion forum post about the pros and cons of using social media.",
        "A brief news report on a local event or an environmental issue.",
        "A short biography of a famous Swedish artist or athlete.",
        "Instructions for a complex task, like assembling furniture or setting up a computer program."
    ],
    "B2": [
        "A formal report on a recent business meeting, including different viewpoints and outcomes.",
        "An opinion piece on a controversial topic, such as public transportation or education reform.",
        "An excerpt from a novel or a detailed short story with more complex characters and plot.",
        "A research summary on a scientific topic, such as renewable energy or climate change.",
        "A detailed travel guide describing different regions of Sweden, including historical context and local customs.",
        "A detailed interview with a professional discussing their career and challenges in their field."
    ],
    "C1": [
        "A literary analysis of a Swedish poem or a short story.",
        "An academic article on a specialized subject, such as urban planning or cognitive psychology.",
        "A critique of a film or a play, discussing its themes, symbolism, and a director's style.",
        "A philosophical essay exploring abstract concepts like freedom or truth.",
        "A legal document or a policy paper outlining new regulations.",
        "A speech or a lecture transcript on a complex social or political issue."
    ],
    "C2": [
        "An excerpt from a scholarly monograph on a highly specialized topic.",
        "A complex satirical piece or a political cartoon analysis.",
        "A detailed technical manual for a piece of advanced machinery.",
        "A long-form journalistic report that synthesizes information from multiple sources.",
        "A piece of classical literature or a complex play by a notable author.",
        "A formal dissertation abstract or a research proposal summary."
    ]
    }
    content = """
    You are an expert in teaching Swedish. You are really careful to not make any mistakes and always double-check your work.
    You are also really comprehensive and thorough in your teaching.
    Your main mission is to help students to practice reading comprehension.
    Higher levels should have more complex vocabulary and sentence structures and more advanced topics.
    Lower levels should have simpler vocabulary and sentence structures and more basic topics.
    A variety of vocabulary and sentence structures to help students improve their reading and comprehension skills should be included.
    6 questions should be generated based on the paragraph to test the students' understanding.
    The questions should be suitable for students at the specified level of the CEFR.
    The questions should be paraphrased and not directly copied from the paragraph.
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
    Your main mission:
    """
    content += f"Generate a {random.choice(reading_topics[level.split("-")[0]]+reading_topics[level.split("-")[1]])}.The reading exercises should be suitable for students at the sepcified level of the Common European Framework of Reference for Languages (CEFR). Be creative but still adhere to the text's mentioned function. The level of your paragraph must be {level}."
    return content
def generate_exercise(level):
    print(level)
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", contents= paragraph_instructions(level))
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