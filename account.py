from hashlib import md5


class Account:
    def __init__(self):
        self.__username = ""
        self.__user_line = 1

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, new_username):
        self.__username = new_username

    @property
    def user_line(self):
        return self.__user_line

    @user_line.setter
    def user_line(self, new_user_line):
        self.__user_line = new_user_line

    def signup(self):
        print("---Sign Up---")
        account_file = open("username_password.txt", "r+")
        account_information = account_file.readlines()
        username = input("Username: ")
        while True:
            password = input("Password: ")
            if len(password) >= 8 and password.isascii() \
                    and any(char.isnumeric() for char in password) \
                    and any(char.isupper() for char in password):
                for user in account_information:
                    if username == user.split(",")[0]:
                        print("This username has already been signed up.")
                        print()
                        return None
                break
            else:
                print("Password must be longer or equal to 8 characters.")
                print("Password must contains Uppercase and Number.")
        print(f"{username} is now registered.")
        print()
        password = (md5(password.encode())).digest()
        account_file.write(username + "," + str(password) + "," + "0" + "\n")
        account_file.close()
        self.username = username

    def login(self):
        print("---Log In---")
        account_information = open("username_password.txt", "r").readlines()
        username = input("Username: ")
        password = input("Password: ")
        check = 0
        password = (md5(password.encode())).digest()
        for user in account_information:
            if username == user.split(",")[0] and str(password) == \
                    user.split(",")[1]:
                check = 1
                self.user_line = account_information.index(user)
            elif username == user.split(",")[0]:
                check = 2
        if check == 1:
            self.username = username
            print("Log In Successfully")
            print()
        elif check == 2:
            print("Your password is wrong.")
            print(
                "Make sure that you use the same password you signed up with.")
            print()
        else:
            print("Your account has not been signed up yet.")
            print("Please Sign up first")
            print()

    def write_score(self, name, score):
        account_file = open("username_password.txt", "r+")
        account_information = account_file.readlines()
        for line in account_information:
            if line.split(",")[0] == name \
                    and score > int(line.split(",")[2]):
                edited_line = line.split(",")[0] + "," + \
                              line.split(",")[1] + "," + \
                              str(score) + "\n"
                account_file.seek(0)
                account_file.truncate()
                account_file.writelines(
                    account_information[0:account_information.index(line)])
                account_file.writelines(edited_line)
                account_file.writelines(
                    account_information[account_information.index(line) + 1:])
                account_file.close()
                break

    def get_rank(self, name):
        account_information = open("username_password.txt", "r+").readlines()
        unsorted_rank = {user.split(",")[0]: int(user.split(",")[2])
                         for user in account_information}
        rank = dict(sorted(unsorted_rank.items(), key=lambda item: item[1],
                           reverse=True))
        player_rank = [player for player in rank.keys()]
        return player_rank.index(name) + 1

    def get_top5(self):
        account_information = open("username_password.txt", "r+").readlines()
        unsorted_rank = {user.split(",")[0]: int(user.split(",")[2])
                         for user in account_information}
        rank = dict(sorted(unsorted_rank.items(), key=lambda item: item[1],
                           reverse=True))
        player_rank = [player for player in rank.keys()]
        for index in range(5):
            try:
                player = player_rank[index]
                print(f"{index + 1}) {player}: {rank[player]}")
            except IndexError:
                print(f"{index + 1})")
