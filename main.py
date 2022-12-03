from account import Account
from game import Game
from time import sleep

story_lines = ["A long time yet to come in a galaxy very very close...",
               "Galaxoid, A Space Terrorist has spread its power around "
               "the galaxy.",
               "It is a dark time for the Empire.",
               "An Endless War has begun.",
               "Your job is to end this war."]


def main(story):
    """ Run Main program """
    while True:
        print("Please Sign up or Log in to play the game.")
        print("1. Sign up")
        print("2. Log in")
        user = Account()
        menu = input("Enter your Choice: ")
        print()
        if menu == "1":
            user.signup()
            if user.username != "":
                print(f"Welcome {user.username}.")
        elif menu == "2":
            user.login()
            if user.username != "":
                print(f"Welcome back, {user.username}.")
        else:
            print("Please Input The Correct Choice")
            print()
        if user.username != "":
            break
    # Print out story
    for line in story:
        print(line)
        sleep(2)
    start_choice = input("Do you want to join this war? (Y/N): ").upper()
    while start_choice != "Y" and start_choice != "N":
        start_choice = input("Do you want to join this war? (Y/N): ").upper()
    if start_choice == "Y":
        print()
        print("--How to play--")
        print("Press Arrow keys to Move.")
        print("Press Space bar to Shoot.")
        print("Press ESC to Quit.")
        print()
        print("Yellow Orb can be obtained to increase your life(<=5).")
        print("Enemies will come endlessly, Be prepared.")
        print()
        ready_choice = input("Are you ready? (Y): ").upper()
        while ready_choice != "Y":
            ready_choice = input("Are you ready? (Y): ").upper()
        # Start the game
        main_game = Game(user.username)
        main_game.play_game()
        # Record user high score
        user.write_score(user.username, main_game.player.score)
        print()
        print("--Round Summary--")
        print(f"Player: {user.username}")
        print(f"Score: {main_game.player.score}")
        print(f"Accuracy: {main_game.player.accuracy:.2f} %")
        print(f"Current Rank: {user.get_rank(user.username)}")
        print()
        print("|-------------Leaderboard-------------|")
        user.get_top5()
        print("|-------------------------------------|")
    elif start_choice == "N":
        print()
        print("|-------------Leaderboard-------------|")
        user.get_top5()
        print("|-------------------------------------|")
        print()
        print("Please Come Back Later")


if __name__ == '__main__':
    main(story_lines)
