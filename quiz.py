class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

def display(self):
    print(f"\n{self.question}\n")
    for i, choice in enumerate(self.choices, start=1):
        print(f"  {i}. {choice}")

def check_answer(self, user_input):
    return user_input == self.answer

def to_dict(self):
    return {
        "question": self.question,
        "choices": self.choices,
        "answer": self.answer
    }

@staticmethod
def from_dict(data):
    return Quiz(
        question=data["question"],
        choices=data["choices"],
        answer=data["answer"]
    )