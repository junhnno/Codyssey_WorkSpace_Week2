## clone 실습

# 나는 어떤 사람일까요?

## 프로젝트 개요
'황준호'에 관한 정보를 퀴즈로 맞추는 터미널 기반 퀴즈 게임입니다.
퀴즈 풀기, 추가, 목록 확인, 점수 확인 기능을 제공하며
프로그램을 종료해도 데이터가 유지됩니다.

## 퀴즈 주제 선정 이유
나에 대한 정보를 퀴즈로 만들어 동료들이 알아갈 수 있게 주제 선정하게 되었다.

## 실행 방법
```bash
python main.py
```

## 기능 목록
| 기능 | 설명 |
|------|------|
| 퀴즈 풀기 | 저장된 퀴즈를 순서대로 풀고 결과 확인 |
| 퀴즈 추가 | 새로운 퀴즈를 등록하고 파일에 저장 |
| 퀴즈 목록 | 등록된 퀴즈 전체 목록 확인 |
| 점수 확인 | 최고 점수 확인 |

## 파일 구조
```
quiz-game/
├── main.py       # 진입점
├── quiz.py       # Quiz 클래스
├── game.py       # QuizGame 클래스
├── state.json    # 데이터 저장 파일 (자동 생성)
├── .gitignore
└── README.md
```

## 데이터 파일 설명 (state.json)
- **경로**: 프로젝트 루트/state.json
- **역할**: 퀴즈 데이터와 최고 점수를 저장하여 프로그램 종료 후에도 데이터 유지
- **인코딩**: UTF-8
- **스키마**:
```json
{
    "quizzes": [
        {
            "question": "준호의 키는?",
            "choices": ["175cm", "177cm", "179cm", "181cm"],
            "answer": 3
        }
    ],
    "best_score": 80
}
```

### main.py
```
from game import QuizGame

if __name__ == "__main__":
    game = QuizGame()
    game.load()
    game.run()
```
## game.py
```
import json
import os
from quiz import Quiz

DEFAULT_QUIZZES = [
    Quiz(
        question="준호의 키는?",
        choices=["175cm", "177cm", "179cm", "181cm"],
        answer=3
    ),
    Quiz(
        question="준호가 가장 좋아하는 음식은?",
        choices=["삼겹살", "족발", "치킨", "라면"],
        answer=4
    ),
    Quiz(
        question="준호의 폰 케이스 캐릭터는?",
        choices=["라이언", "패트와 매트", "미니언즈", "스폰지밥"],
        answer=2
    ),
    Quiz(
        question="준호가 가장 잘하는 스포츠는?",
        choices=["볼링", "농구", "당구", "탁구"],
        answer=3
    ),
    Quiz(
        question="준호가 나온 군대는?",
        choices=["육군", "공군", "해군", "해병대"],
        answer=4
    ),
]

class QuizGame:
    def __init__(self):
        self.quizzes = DEFAULT_QUIZZES[:]
        self.best_score = 0

    def show_menu(self):
        print("\n========================================")
        print("         나는 어떤 사람일까요? ")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 삭제")
        print("4. 퀴즈 목록")
        print("5. 점수 확인")
        print("6. 종료")
        print("========================================")

    def run(self):
        while True:
            try:
                self.show_menu()
                choice = input("선택: ").strip()

                if choice == "":
                    print("⚠️ 입력값이 없습니다. 1-6 사이의 숫자를 입력하세요.")
                    continue
                if not choice.isdigit():
                    print("⚠️ 잘못된 입력입니다. 1-6 사이의 숫자를 입력하세요.")
                    continue

                choice = int(choice)

                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.delete_quiz()
                elif choice == 4:
                    self.show_list()
                elif choice == 5:
                    self.show_score()
                elif choice == 6:
                    print("게임을 종료합니다.")
                    self.save()
                    break
                else:
                    print("⚠️ 잘못된 입력입니다. 1-6 사이의 숫자를 입력하세요.")

            except KeyboardInterrupt:
                print("\n\n프로그램을 종료합니다.")
                self.save()
                break
            except EOFError:
                print("\n\n입력 스트림이 종료되었습니다.")
                self.save()
                break

    def play(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        score = 0

        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"\n----------------------------------------")
            print(f"[문제 {i}]")
            quiz.display()

            while True:
                try:
                    user_input = input("\n정답 입력: ").strip()

                    if user_input == "":
                        print("⚠️ 입력값이 없습니다. 1-4 사이의 숫자를 입력하세요.")
                        continue
                    if not user_input.isdigit():
                        print("⚠️ 잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
                        continue

                    user_input = int(user_input)

                    if user_input < 1 or user_input > 4:
                        print("⚠️ 잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
                        continue

                    break

                except KeyboardInterrupt:
                    print("\n\n퀴즈를 종료합니다.")
                    self.save()
                    return

            if quiz.check_answer(user_input):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답입니다! 정답은 {quiz.answer}번입니다.")

        total = len(self.quizzes)
        percent = int(score / total * 100)

        print(f"\n========================================")
        print(f"🏆 결과: {total}문제 중 {score}문제 정답! ({percent}점)")

        if percent > self.best_score:
            self.best_score = percent
            print("🎉 새로운 최고 점수입니다!")

        print(f"========================================")
        self.save()

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")

        question = input("문제를 입력하세요: ").strip()
        if question == "":
            print("⚠️ 문제를 입력해야 합니다.")
            return

        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"선택지 {i}: ").strip()
                if choice == "":
                    print("⚠️ 선택지를 입력해야 합니다.")
                    continue
                choices.append(choice)
                break

        while True:
            try:
                answer = input("정답 번호 (1-4): ").strip()

                if answer == "":
                    print("⚠️ 입력값이 없습니다. 1-4 사이의 숫자를 입력하세요.")
                    continue
                if not answer.isdigit():
                    print("⚠️ 잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
                    continue

                answer = int(answer)

                if answer < 1 or answer > 4:
                    print("⚠️ 잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
                    continue

                break

            except KeyboardInterrupt:
                print("\n\n퀴즈 추가를 취소합니다.")
                return

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save()
        print("✅ 퀴즈가 추가되었습니다!")

    def delete_quiz(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        self.show_list()

        while True:
            try:
                number = input("\n삭제할 퀴즈 번호를 입력하세요: ").strip()

                if number == "":
                    print("⚠️ 입력값이 없습니다.")
                    continue
                if not number.isdigit():
                    print("⚠️ 잘못된 입력입니다. 숫자를 입력하세요.")
                    continue

                number = int(number)

                if number < 1 or number > len(self.quizzes):
                    print(f"⚠️ 잘못된 입력입니다. 1-{len(self.quizzes)} 사이의 숫자를 입력하세요.")
                    continue

                break

            except KeyboardInterrupt:
                print("\n\n퀴즈 삭제를 취소합니다.")
                return

        deleted = self.quizzes.pop(number - 1)
        self.save()
        print(f"✅ [{deleted.question}] 퀴즈가 삭제되었습니다!")

    def show_list(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print("----------------------------------------")

    def show_score(self):
        if self.best_score == 0:
            print("\n⚠️ 아직 퀴즈를 풀지 않았습니다.")
            return

        print(f"\n🏆 최고 점수: {self.best_score}점")

    def save(self):
        try:
            data = {
                "quizzes": [quiz.to_dict() for quiz in self.quizzes],
                "best_score": self.best_score
            }
            with open("state.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"⚠️ 저장 중 오류가 발생했습니다: {e}")

    def load(self):
        if not os.path.exists("state.json"):
            print("📂 기본 퀴즈 데이터로 시작합니다.")
            return

        try:
            with open("state.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data["quizzes"]]
            self.best_score = data["best_score"]
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
        except (json.JSONDecodeError, KeyError):
            print("⚠️ 데이터 파일이 손상되었습니다. 기본 퀴즈 데이터로 초기화합니다.")
            self.quizzes = DEFAULT_QUIZZES[:]
            self.best_score = 0
        except Exception as e:
            print(f"⚠️ 불러오기 중 오류가 발생했습니다: {e}")
```

##quiz.py
```
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
```

## 감사합니다!

