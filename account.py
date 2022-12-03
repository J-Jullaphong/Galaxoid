from hashlib import md5
from json import dump, load


class Account:
    def __init__(self):
        """ Create User Account """
        self.__username = ""

    @property
    def username(self):
        """ Username Property represents Username of the account """
        return self.__username

    @username.setter
    def username(self, new_username):
        """ Sets username of the account """
        self.__username = new_username

    def signup(self):
        """ Register User Account and Save into accounts.json file """
        try:
            with open("accounts.json", "r") as account_data:
                accounts = load(account_data)
            print("---Sign Up---")
            username = input("Username: ")
            while True:
                password = input("Password: ")
                # Check Password Strength
                if len(password) >= 8 and password.isascii() \
                        and any(char.isnumeric() for char in password) \
                        and any(char.isupper() for char in password):
                    # Check if the username is already signed up
                    if username in accounts:
                        print("This username has already been signed up.")
                        print()
                        return None
                    break
                else:
                    print("Password must be longer or equal to 8 "
                          "characters.")
                    print("Password must contain Uppercase and Number.")
            print(f"{username} is now registered.")
            print()
            # Hash the Password before storing into accounts.json file
            password = str(md5(password.encode()).digest())
            account_info = {
                username: {
                    "password": password,
                    "high_score": 0,
                }
            }
            accounts.update(account_info)
            with open("accounts.json", "w") as account_data:
                dump(accounts, account_data, indent=4)
            self.username = username
        # Catch FileNotFoundError, then create accounts.json file
        except FileNotFoundError:
            with open("accounts.json", "w") as account_data:
                account_info = {
                    "username": {
                        "password": "password",
                        "high_score": 0,
                    }
                }
                dump(account_info, account_data, indent=4)
            self.signup()

    def login(self):
        """ Let user log in with existing account in accounts.json file """
        try:
            with open("accounts.json", "r") as account_data:
                accounts = load(account_data)
            print("---Log In---")
            username = input("Username: ")
            password = input("Password: ")
            password = str(md5(password.encode()).digest())
            # Check if the username existed in accounts.json file or not
            if username in accounts:
                # Check if the password match to the existed user
                if accounts[username]["password"] == password:
                    self.username = username
                    print("Log In Successfully")
                    print()
                else:
                    print("Your password is wrong.")
                    print("Make sure that you use the same password you "
                          "signed up with.")
                    print()
            else:
                print("Your account has not been signed up yet.")
                print("Please Sign Up First")
                print()
        except FileNotFoundError:
            print("Account Data File Not Found")
            print("Please Sign Up First")
            print()

    def write_score(self, name, score):
        """ Save User's score into accounts.json file """
        try:
            with open("accounts.json", "r") as account_data:
                accounts = load(account_data)
            # Check if the score is higher than the recorded high score
            if score > int(accounts[name]["high_score"]):
                accounts[name]["high_score"] = score
            with open("accounts.json", "w") as account_data:
                dump(accounts, account_data, indent=4)
        except FileNotFoundError:
            print("Account Data File Not Found")
            print()

    def get_rank(self, name):
        """ Receive Player's current rank from accounts.json file """
        try:
            with open("accounts.json", "r") as account_data:
                accounts = load(account_data)
            # Get unsorted rank list from accounts.json file
            unsorted_rank = {user: int(accounts[user]["high_score"])
                             for user in accounts if user != "username"}
            # Sort users' rank by high score
            rank = dict(sorted(unsorted_rank.items(), key=lambda item: item[1],
                               reverse=True))
            player_rank = [player for player in rank.keys()]
            # Return the rank of player
            return player_rank.index(name) + 1
        except FileNotFoundError:
            print("Account Data File Not Found")
            print()

    def get_top5(self):
        """ Receive Current Top 5 players from accounts.json file """
        try:
            with open("accounts.json", "r") as account_data:
                accounts = load(account_data)
            # Get unsorted rank list from accounts.json file
            unsorted_rank = {user: int(accounts[user]["high_score"])
                             for user in accounts if user != "username"}
            # Sort users' rank by high score
            rank = dict(sorted(unsorted_rank.items(), key=lambda item: item[1],
                               reverse=True))
            player_rank = [player for player in rank.keys()]
            print("|  Rank  |    Pilot    |  High Score  |")
            # Print out current top 5 players
            for index in range(5):
                try:
                    player = player_rank[index]
                    print(f"|{index + 1:^8}|{player:^13}|{rank[player]:^12}  |")
                except IndexError:
                    print(f"|{index + 1:^8}|" + " " * 13 + "|" + " " * 14 + "|")
        except FileNotFoundError:
            print("Account Data File Not Found")
            print()
