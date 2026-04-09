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

def show_menu(self):
    print("\n========================================")
    print("         저에 대해서 맞춰보세요 ")
    print("========================================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("========================================")

def run(self):
    while True:
        try:
            self.show_menu()
            choice = input("선택: ").strip()

            if choice == "":
                print("⚠️ 입력값이 없습니다. 1-5 사이의 숫자를 입력하세요.")
                continue
            if not choice.isdigit():
                print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
                continue

            choice = int(choice)

            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_list()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("게임을 종료합니다.")
                self.save()
                break
            else:
                print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")

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


def show_list(self):
    if not self.quizzes:
        print("⚠️ 등록된 퀴즈가 없습니다.")
        return

    print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
    print("----------------------------------------")
    for i, quiz in enumerate(self.quizzes, start=1):
        print(f"[{i}] {quiz.question}")
    print("----------------------------------------")