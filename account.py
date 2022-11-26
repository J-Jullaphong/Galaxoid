from hashlib import md5
from json import dump, load


class Account:
    def __init__(self):
        self.__username = ""

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, new_username):
        self.__username = new_username

    def signup(self):
        try:
            with open("accounts.json", "r") as account_data:
                accounts = load(account_data)
            print("---Sign Up---")
            username = input("Username: ")
            while True:
                password = input("Password: ")
                if len(password) >= 8 and password.isascii() \
                        and any(char.isnumeric() for char in password) \
                        and any(char.isupper() for char in password):
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
        try:
            with open("accounts.json", "r") as account_data:
                accounts = load(account_data)
            print("---Log In---")
            username = input("Username: ")
            password = input("Password: ")
            check = 0
            password = str(md5(password.encode()).digest())
            for user in accounts:
                if username == user and str(password) == \
                        accounts[user]["password"]:
                    check = 1
                elif username == user:
                    check = 2
            if check == 1:
                self.username = username
                print("Log In Successfully")
                print()
            elif check == 2:
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
        try:
            with open("accounts.json", "r") as account_data:
                accounts = load(account_data)
                for user in accounts:
                    if name == user and score > \
                            int(accounts[user]["high_score"]):
                        accounts[user]["high_score"] = score
            with open("accounts.json", "w") as account_data:
                dump(accounts, account_data, indent=4)
        except FileNotFoundError:
            print("Account Data File Not Found")
            print()

    def get_rank(self, name):
        try:
            with open("accounts.json", "r") as account_data:
                accounts = load(account_data)
            unsorted_rank = {user: int(accounts[user]["high_score"])
                             for user in accounts if user != "username"}
            rank = dict(sorted(unsorted_rank.items(), key=lambda item: item[1],
                               reverse=True))
            player_rank = [player for player in rank.keys()]
            return player_rank.index(name) + 1
        except FileNotFoundError:
            print("Account Data File Not Found")
            print()

    def get_top5(self):
        try:
            with open("accounts.json", "r") as account_data:
                accounts = load(account_data)
            unsorted_rank = {user: int(accounts[user]["high_score"])
                             for user in accounts if user != "username"}
            rank = dict(sorted(unsorted_rank.items(), key=lambda item: item[1],
                               reverse=True))
            player_rank = [player for player in rank.keys()]
            print("|  Rank  |    Name    |  High Score  |")
            for index in range(5):
                try:
                    player = player_rank[index]
                    print(f"|{index + 1:^8}|{player:^12}|{rank[player]:^12}  |")
                except IndexError:
                    print(f"|{index + 1:^8}|" + " " * 12 + "|" + " " * 14 + "|")
        except FileNotFoundError:
            print("Account Data File Not Found")
            print()
