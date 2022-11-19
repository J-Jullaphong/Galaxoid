from account import Account
from game import Game


def main():
    while True:
        print("Please Sign up or Log in to play the game.")
        print("1. Sign up")
        print("2. Log in")
        user = Account()
        try:
            menu = int(input("Enter your Choice: "))
            if menu == 1:
                print()
                user.signup()
            elif menu == 2:
                print()
                user.login()
            else:
                print("Please Input The Correct Choice")
                print()
        except ValueError:
            print("Please Input The Correct Choice")
            print()
        if user.username != "":
            break
    print(f"Welcome {user.username}.")
    print("This Is Galaxoid, An Endless Space Shooter Game.")
    print("Your Task Is To Get The Highest Score To Become The Best Pilot.")
    start_choice = input("Start the game (Y/N): ").upper()
    while start_choice != "Y" and start_choice != "N":
        start_choice = input("Start the game (Y/N): ").upper()
    if start_choice == "Y":
        main_game = Game(user.username)
        main_game.play_game()
        user.write_score(user.username, main_game.player.score)
        print()
        print("--Round Summary--")
        print(f"Player: {user.username}")
        print(f"Score: {main_game.player.score}")
        print(f"Current Rank: {user.get_rank(user.username)}")
        print()
        print("--Leaderboard--")
        user.get_top5()
    elif start_choice == "N":
        print("Please Come Back Later")


if __name__ == '__main__':
    main()
