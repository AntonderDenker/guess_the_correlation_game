# guess the correlation
print("The application needs up to 15 seconds to start...")

import threading
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import colorama as color
import random
import requests
import os
import pygetwindow
import ctypes
import sys
import mysql.connector

# database
db_name = "db_390976_24"
db = mysql.connector.connect(
    host="antondereroberer.lima-db.de",
    user="USER390976_gtc",
    password="XerXes0909#",
    database=db_name
)

db_cursor = db.cursor()


def insert_session(points, name):
    statement = (f"INSERT INTO session"
                 "(points, name)"
                 "VALUES (%s, %s)")
    values = (points, name)
    db_cursor.execute(statement, values)
    db.commit()




def check_github_release(repo_owner, repo_name):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(api_url)
    if response.status_code == 200:
        release = response.json()
        latest_version = release['tag_name']
        # Compare the latest version with the current version of your application
        # and determine if an update is available
        return latest_version
    else:
        # Handle error response
        return None


new_version = check_github_release("AntonderDenker", "guess_the_correlation_game")

version = "v1.0.7"

color.init()
matplotlib.interactive(True)
plt.ion()

# formats
forms = {
    "RESET": color.Style.RESET_ALL,
    "GREEN": color.Fore.GREEN,
    "RED": color.Fore.RED,
    "BRIGHT": color.Style.BRIGHT,
}


def set_format(text, form):
    return f"{forms[form]}{text}{forms['RESET']}"


ctypes.windll.kernel32.SetConsoleTitleW("guess_the_correlation")
console_window = pygetwindow.getWindowsWithTitle('guess_the_correlation')[0]


def get_banner(text):
    return f"----------{text}---------"


def random_data(correlation_coefficient):
    x = np.random.rand(100)
    y = correlation_coefficient * x + np.random.randn(100) * np.sqrt((1 - correlation_coefficient ** 2) * np.var(x))
    x = x * 100
    y = y * 100

    return [x, y]


def get_r():
    return float(round(random.uniform(0, 1), 2))


def create_plot(data):
    plt.scatter(data[0], data[1])
    plt.show()


def clear_console():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')


def print_tutorial():
    print(f"Welcome to {set_format('Guess The Correlation', 'BRIGHT')}!")
    print(
        f"{color.Style.DIM}developed by Anton Hauffe, inspired by https://www.guessthecorrelation.com/ {forms['RESET']}")
    print(f"{set_format(get_banner('Tutorial'), 'BRIGHT')}")
    print("-> Wait until the scatterplot appears")
    print("-> I recommend to drag the console window to the right of your screen since the appearing plot could "
          "eventually cover the console.")
    print("-> guess the correlation coefficient between 0 and 1")
    print(f"-> if you are close, {set_format('(+-0.1)', 'GREEN')} you get {set_format('1', 'GREEN')} point")
    print(f"-> if you are closer, {set_format('(+-0.05)', 'GREEN')}) you get {set_format('2', 'GREEN')} points")
    print(f"-> if you very close, {set_format('(+-0.02)', 'GREEN')} you get {set_format('5', 'GREEN')} points")
    print(f"-> if you are {set_format('exact', 'GREEN')}, you get {set_format('10', 'GREEN')} points")
    print(f"-> if you missed, you lose {set_format('1 of 3', 'RED')} health points")
    print(f"{set_format('GOOD LUCK!', 'GREEN')}")
    print(f"{set_format(get_banner('Tutorial End'), 'BRIGHT')}")


class Game:
    def __init__(self, name):
        self.health = None
        self.points = None
        self.name = name

        self.playing = True
        self.history = []

        # Rules
        self.point_distribution = [
            {"reward": 10, "deviation": 0},
            {"reward": 5, "deviation": 0.02},
            {"reward": 2, "deviation": 0.05},
            {"reward": 1, "deviation": 0.1},
        ]
        self.max_health = 3

    def game_loop(self):
        while self.playing:
            plt.close()
            clear_console()
            # generate data and r
            rnd_r = get_r()
            data = random_data(rnd_r)
            create_plot(data)
            console_window.activate()
            # ask for users guess
            loop = True
            while loop:
                guess = input(f"{set_format('Guess the correlation coefficient of this data:', 'BRIGHT')}")
                guess = guess.replace(",", ".")
                if guess.isnumeric() or (guess.count('.') == 1 and guess.replace('.', '').isnumeric()):
                    guess = float(guess)
                    if 0 <= guess <= 1:
                        loop = False
                        break
                print("Only numbers between 0 and 1 allowed")

            # check if guess was right
            print(f"Your Guess: {set_format(guess, 'BRIGHT')}")
            print(f"r: {set_format(rnd_r, 'BRIGHT')}")
            print(f"Difference: {set_format(round((guess - rnd_r), 2), 'BRIGHT')}")
            self.check_guess(guess, rnd_r)
            input("Next plot? [press enter]")

    def start(self):
        self.points = 0
        self.health = self.max_health
        self.playing = True
        game_loop = threading.Thread(target=self.game_loop())
        game_loop.start()

    def update_points(self, points):
        self.points += points
        print(forms[
                  "GREEN"] + f"Congratulation, you earned {forms['GREEN']}{points}{forms['RESET']}{forms['GREEN']} points!" +
              forms['RESET'])

    def update_health(self, value):
        self.health += value
        print(
            f"{forms['RED']}The {set_format('difference', 'BRIGHT')}{forms['RED']} between your guess and r was too large{forms['RESET']}")
        if self.health == 0:
            self.game_over()
        else:
            print(forms[
                      'RED'] + f"Oh no! your health changed to {forms['BRIGHT']}{str(self.health) + '/' + str(self.max_health)}{forms['RESET'] + forms['RED']}!" +
                  forms['RESET'])

    def game_over(self):
        self.playing = False
        self.history.append(self.points)
        print(f"{set_format('You lost all your health points!', 'RED')}")
        print(f"{set_format(get_banner('Statistics'), 'BRIGHT')}")
        print(f"Points: {set_format(self.points, 'GREEN')}")
        print(f"{set_format(get_banner('Statistics End'), 'BRIGHT')}")
        insert = threading.Thread(target=insert_session(self.points, self.name))
        insert.start()
        loop = True
        while loop:
            play_again = input(f"If you want to play again type [y] -> [enter] or if not type [n] -> [enter]")
            if play_again == "y":
                self.start()
                loop = False
            elif play_again == "n":
                print(f"{forms['BRIGHT']}{get_banner('History')}{forms['RESET']}")
                for i in range(len(self.history)):
                    print(f"{i+1}. Game: {set_format(self.history[i], 'GREEN')}")
                print(f"{forms['BRIGHT']}{get_banner('History End')}{forms['RESET']}")
                input("Press [enter] to close")
                sys.exit()
            else:
                print("only [y] or [n] accepted")

    def check_guess(self, guess, r):
        right_guess = False
        for i in range(len(self.point_distribution)):
            deviation = self.point_distribution[i]['deviation']
            lower_barrier = round((r - deviation), 2)
            upper_barrier = round((r + deviation), 2)
            # print(f"{lower_barrier} + {upper_barrier}")
            if lower_barrier <= guess <= upper_barrier:
                self.update_points(self.point_distribution[i]['reward'])
                print(f"Health: {set_format(str(self.health) + '/' + str(self.max_health), 'RED')}")
                print(f"Points: {set_format(self.points, 'GREEN')}")
                right_guess = True
                break

        if not right_guess:
            self.update_health(-1)


clear_console()
print(f"{set_format(get_banner(version), 'BRIGHT')}")
if version != new_version:
    print(
        f"{forms['RED']}There is a new version ({new_version}) of the game. Please update using the 'installer_updater.exe'{forms['RESET']}")
print_tutorial()
input("[Press Enter to start the game]")
username = input("Enter your name:")
game = Game(username)
game.start()
