import random
import os
api_key = os.getenv("GEMINI_API_KEY")

import ast
from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=api_key)

topics = [
    "Mathematics", "Science", "History", "Geography", "Literature",
    "Sports", "Music", "Movies", "Technology", "Art",
    "Politics", "Biology", "Physics", "Chemistry", "Computer Science",
    "General Knowledge", "Economics", "Languages", "Space", "Mythology"
]

def generate_quiz_questions(topic, num_questions=10):
    prompt = f"""Generate {num_questions} multiple-choice quiz questions on the topic '{topic}'. 
Format each question like this in a Python list of dictionaries:

[
  {{
    "question": "Question text?",
    "options": ["A. option1", "B. option2", "C. option3", "D. option4"],
    "answer": "A"
  }},
  ...
]

Only output the Python list exactly like above.
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

def clean_response_text(text):
    # Remove markdown code blocks if present
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return text

def main():
    print("Welcome to the AI Quiz Game!")

    def choice_topic():
        chosen = random.sample(topics, 5)
        print("\nChoose your quiz topic from the following:")
        for i, t in enumerate(chosen, 1):
            print(f"{i}. {t}")
        return chosen

    chosen_topics = choice_topic()

    while True:
        reroll = input("Do you want to reroll the topics? (Y/N): ").strip().upper()
        if reroll == 'Y':
            chosen_topics = choice_topic()
        elif reroll == 'N':
            break
        else:
            print("Invalid input. Please enter Y or N.")

    while True:
        try:
            choice = int(input("\nEnter the number of the topic you want to play: "))
            if 1 <= choice <= 5:
                quiz_topic = chosen_topics[choice - 1]
                break
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print(f"\nGenerating quiz questions on: {quiz_topic} ... Please wait.")
    questions_text = generate_quiz_questions(quiz_topic, 5)
    questions_text = clean_response_text(questions_text)

    try:
        questions = ast.literal_eval(questions_text)
    except Exception:
        print("Failed to parse questions from AI response. Here's the raw output:")
        print(questions_text)
        return

    print(f"\nQuiz on {quiz_topic} starts now!\n")

    score = 0
    for i, q in enumerate(questions, 1):
        print(f"Q{i}: {q['question']}")
        for option in q['options']:
            print(option)

        while True:
            answer = input("Your answer (A/B/C/D): ").strip().upper()
            if answer in ['A', 'B', 'C', 'D']:
                break
            else:
                print("Please enter A, B, C, or D.")

        if answer == q['answer'].upper():
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer was {q['answer']}.\n")

    print(f"Quiz finished! Your score: {score} out of {len(questions)}")

if __name__ == "__main__":
    main()
