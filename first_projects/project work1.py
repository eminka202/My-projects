import random

def get_computer_choice():
    return random.choice(["камень", "ножницы", "бумага"])


def determine_winner(player, computer):
    if player == computer:
        return "draw"
    elif (
        (player == "камень" and computer == "ножницы") or
        (player == "ножницы" and computer == "бумага") or
        (player == "бумага" and computer == "камень")
    ):
        return "player"
    else:
        return "computer"


def main():
    print("Добро пожаловать в игру «Камень, Ножницы, Бумага»!")
    print("Правила:")
    print("Камень бьёт ножницы")
    print("Ножницы бьют бумагу")
    print("Бумага бьёт камень")
    print("Игра идёт до 3 очков\n")

    player_score = 0
    computer_score = 0

    while player_score !=3 and computer_score !=3:
        player_choice = input("Ваш выбор (камень / ножницы / бумага): ").lower()

        if player_choice not in ["камень", "ножницы", "бумага"]:
            print("Неверный ввод, попробуйте ещё раз\n")
            continue

        computer_choice = get_computer_choice()
        print("Компьютер выбрал:", computer_choice)

        winner = determine_winner(player_choice, computer_choice)

        if winner == "draw":
            print("Ничья!")
        elif winner == "player":
            print("Вы выиграли раунд!")
            player_score += 1
        else:
            print("Компьютер выиграл раунд!")
            computer_score += 1

        print(f"Счёт: Вы {player_score} — Компьютер {computer_score}\n")

    print("Игра окончена!")
    if player_score == 3:
        print(" Вы победили!")
    else:
        print(" Победил компьютер")