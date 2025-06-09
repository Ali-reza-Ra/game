from config import GAME_CHOICES, RULES, scoreboard
from random import choice


def get_user_choice():
    """
    get and validate user input, recursively
    :return: user_input
    """
    while True:
        user_input = input("Please enter you're choice (r, p, s): ")
        if user_input in GAME_CHOICES:
            return user_input
        print("oops!... wrong choice please try again: ")


def get_system_choice():
    """
    choice random from GAME_CHOICES
    """
    return choice(GAME_CHOICES)


def find_winner(user: str, sys: str):
    """
    receive user and system choice, sort them and compare with game rules if
    they are not the same
    :param user:
    :param sys:
    :return: winner
    """
    match = {user, sys}
    if len(match) == 1:
        return None

    return RULES[tuple(sorted(match))]


def update_scoreboard(result: dict[str: int]):
    """
    Update scoreboard after each hand of the game and show live result
    until now + last hand result
    """

    if result["user"] == 3:
        scoreboard["user"] += 1
        msg = "You win"
    else:
        scoreboard["system"] += 1
        msg = "You lose"

    print("#" * 30)
    print("##", f'user: {scoreboard["user"]}'.ljust(24), "##")
    print("##", f'system: {scoreboard["system"]}'.ljust(24), "##")
    print("##", f'last game: {msg}'.ljust(24), "##")
    print("#" * 30)


def play_again():
    user_input = input("Do you want to play again!?: ")
    if user_input.lower() == "y":
        play()


def play():
    """
    playground
    :return:
    """
    result = {"user": 0, "system": 0}

    while result["user"] < 3 and result["system"] < 3:

        user_choice = get_user_choice()
        system_choice = get_system_choice()
        winner = find_winner(user_choice, system_choice)

        if winner == user_choice:
            msg = "You win"
            result["user"] += 1
        elif winner == system_choice:
            msg = "You lose!"
            result["system"] += 1
        else:
            msg = "Draw"
        print(f"user: {user_choice}\t system: {system_choice}\t result: {msg}")

    update_scoreboard(result)

    play_again()
