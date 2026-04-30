name = input("Welcome! What's your name? ")
print("Hello " + name +"!")

import random

CATEGORY_FILES = {
    1: ("Sport",         "sport.txt"),
    2: ("Science",       "science.txt"),
    3: ("History",       "history.txt"),
    4: ("Geography",     "geography.txt"),
    5: ("Entertainment", "entertainment.txt"),
    6: ("Random",        "random.txt"),
}


def load_questions(filename):
    questions = []
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
    except FileNotFoundError:
        print(f"Warning: Could not find '{filename}'. No questions loaded for this category.")
        return questions

    blocks = content.split("\n\n")
    for block in blocks:
        lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
        
        question_text = None
        options = []
        answer = None

        for line in lines:
            if line.startswith("Q:"):
                question_text = line[2:].strip()
            elif line.startswith("A:"):
                options.append(line[2:].strip())
            elif line.lower().startswith("answer:"):
                answer = line.split(":", 1)[1].strip()

        if question_text and options and answer:
            questions.append({
                "question": question_text,
                "options": options,
                "answer": answer
            })
        
    return questions


def load_all_questions():
    all_questions = {}
    for category_num, (category_name, filename) in CATEGORY_FILES.items():
        all_questions[category_num] = load_questions(filename)
    return all_questions


def roll_dice():
    return random.randint(1, 6)


def ask_question(all_questions, category_num):
    category_name = CATEGORY_FILES[category_num][0]
    questions = all_questions[category_num]

    if not questions:
        print(f"No questions available for {category_name}.")
        return False

    chosen = random.choice(questions)

    print(f"\nCategory: {category_name}")
     print(f"\nQ: {chosen['question']}")

    # Display answer choices as A, B, C, D
    letters = ["A", "B", "C", "D"]
    for i, option in enumerate(chosen["options"]):
        print(f"  {letters[i]}. {option}")

    
    answer_to_letter = {}
    letter_to_answer = {}
    for i, option in enumerate(chosen["options"]):
        answer_to_letter[option.lower()] = letters[i]
        letter_to_answer[letters[i]] = option

    
    answer = input("Your answer (A, B, C or D): ").strip().upper()
    while answer not in letters:
        print("Invalid Response. Please answer again.")
        answer = input("Your answer (A, B, C or D): ").strip().upper()


    correct_letter = answer_to_letter.get(chosen["answer"].lower())
    if answer == correct_letter:
        print("Correct!")
        if scores[roll - 1] == 0:
            scores[roll - 1] = 1
            print(f"You've completed the {category_names[roll]} category!")
    else:
        print(f"Incorrect! The correct answer was {correct_letter}. {chosen['answer']}")


def play_game(all_questions):
    scores = [0, 0, 0, 0, 0, 0]

    print("\n--- Game Start! ---")
    print("Complete all 6 categories to win!\n")

    while True:
        if sum(scores) == 6:
            print("\nCongratulations! You've completed all categories. You win!")
            break

        progress = " | ".join(
            f"{CATEGORY_FILES[i+1][0]}: {'✓' if s else '✗'}"
            for i, s in enumerate(scores)
        )
        print("Progress: " + progress)

        while True:
            instruction = input("\nType 'roll' to roll the dice: ").strip().lower()
            if instruction == "roll":
                break
            print("Invalid Response. Please answer again.")

        roll = roll_dice()
        print(f"You rolled a {roll} — Category: {CATEGORY_FILES[roll][0]}!")

        correct = ask_question(all_questions, roll)

        if correct and scores[roll - 1] == 0:
            scores[roll - 1] = 1
            print(f"You've completed the {CATEGORY_FILES[roll][0]} category!")
        elif correct:
            print(f"You already completed {CATEGORY_FILES[roll][0]}, but great answer!")


def main():
   
    all_questions = load_all_questions()

    while True:
        play_game(all_questions)

        while True:
            play_again = input("\nWould you like to play again? (yes/no): ").strip().lower()
            if play_again in ["yes", "no"]:
                break
            print("Invalid Response. Please answer again.")

        if play_again == "no":
            print("Game End. Thanks for playing!")
            break


if __name__ == "__main__":
    main()