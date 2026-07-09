import random
import time

users = {}  # хранит всех пользователей

# ------------------ РЕГИСТРАЦИЯ ------------------
def register():
    username = input("Введите имя пользователя: ")

    if username in users:
        print("Такое имя уже существует!")
        return

    password = input("Введите пароль (минимум 5 символов, только латинские буквы и цифры): ")

    if len(password) < 5 or not password.isalnum():
        print("Пароль не подходит!")
        return

    users[username] = {
        "password": password,
        "cards": [],
        "notes": []
    }

    print("Регистрация успешна!")


# ------------------ ВХОД ------------------
def login():
    username = input("Имя: ")
    password = input("Пароль: ")

    if username in users and users[username]["password"] == password:
        print("Вход выполнен!")
        return username
    else:
        print("Неверные данные!")
        return None


# ------------------ КАРТОЧКИ ------------------
def add_card(current_user):
    question = input("Введите вопрос: ")
    answer = input("Введите ответ: ")

    users[current_user]["cards"].append({
        "question": question,
        "answer": answer
    })

    print("Карточка добавлена!")


def random_card(current_user):
    cards = users[current_user]["cards"]

    if not cards:
        print("У вас нет карточек!")
        return

    card = random.choice(cards)
    print("Вопрос:", card["question"])
    input("Нажмите Enter чтобы увидеть ответ...")
    print("Ответ:", card["answer"])


# ------------------ ВИКТОРИНА ------------------
def quiz(current_user):
    cards = users[current_user]["cards"]

    if not cards:
        print("Нет карточек для викторины!")
        return

    score = 0
    random.shuffle(cards)

    for card in cards:
        print("\nВопрос:", card["question"])
        start_time = time.time()

        answer = input("Ваш ответ: ")
        end_time = time.time()

        if end_time - start_time > 30:
            print("Время вышло!")
            continue

        if answer.lower() == card["answer"].lower():
            print("Правильно!")
            score += 1
        else:
            print("Неправильно! Правильный ответ:", card["answer"])

    print(f"\nВаш результат: {score} из {len(cards)}")


# ------------------ ЗАМЕТКИ ------------------
def add_note(current_user):
    note = input("Введите текст заметки: ")
    users[current_user]["notes"].append(note)
    print("Заметка сохранена!")


def view_notes(current_user):
    notes = users[current_user]["notes"]

    if not notes:
        print("Нет заметок.")
        return

    for i, note in enumerate(notes):
        print(f"{i+1}. {note}")


def delete_note(current_user):
    view_notes(current_user)
    notes = users[current_user]["notes"]

    if notes:
        num = int(input("Введите номер заметки для удаления: "))
        if 1 <= num <= len(notes):
            notes.pop(num - 1)
            print("Удалено!")


# ------------------ МЕНЮ ПОЛЬЗОВАТЕЛЯ ------------------
def user_menu(current_user):
    while True:
        print("\n--- МЕНЮ ---")
        print("1. Добавить карточку")
        print("2. Случайная карточка")
        print("3. Викторина")
        print("4. Добавить заметку")
        print("5. Посмотреть заметки")
        print("6. Удалить заметку")
        print("7. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            add_card(current_user)
        elif choice == "2":
            random_card(current_user)
        elif choice == "3":
            quiz(current_user)
        elif choice == "4":
            add_note(current_user)
        elif choice == "5":
            view_notes(current_user)
        elif choice == "6":
            delete_note(current_user)
        elif choice == "7":
            break
        else:
            print("Неверный выбор!")


# ------------------ ГЛАВНОЕ МЕНЮ ------------------
while True:
    print("\n=== ГЛАВНОЕ МЕНЮ ===")
    print("1. Регистрация")
    print("2. Вход")
    print("3. Выход")

    choice = input("Выберите действие: ")

    if choice == "1":
        register()
    elif choice == "2":
        user = login()
        if user:
            user_menu(user)
    elif choice == "3":
        print("До свидания!")
        break
    else:
        print("Неверный выбор!")