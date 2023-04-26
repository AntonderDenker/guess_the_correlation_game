# guess the correlation
import threading

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import colorama as color
import random

import os

version = "1.0.4 Alpha"


color.init()
matplotlib.interactive(True)
plt.ion()

# formats

RESET = color.Style.RESET_ALL
GREEN = color.Fore.GREEN
RED = color.Fore.RED
BRIGHT = color.Style.BRIGHT


def get_banner(text):
    return f"----------{text}---------"


def random_data(correlation_coefficient):
    x = np.random.rand(100)
    y = correlation_coefficient * x + np.random.randn(100) * np.sqrt((1 - correlation_coefficient ** 2) * np.var(x))
    x = x * 100
    y = y * 100

    return [x, y]


def create_plot(data):
    plt.scatter(data[0], data[1])
    plt.show()


def clear_console():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')


class Game:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.health = 3
        self.playing = True
        self.history = []

        self.game_loop = threading.Thread(target=self.game_loop())
        self.game_loop.start()

    def game_loop(self):
        while self.playing:
            clear_console()
            rnd_r = round(random.uniform(0, 1), 2)
            rnd_r = float(rnd_r)
            data = random_data(rnd_r)
            create_plot(data)

            guess = input(f"{BRIGHT}Guess the correlation coefficient of this data: {RESET}")
            guess = float(guess)
            print(f"The correlation coefficient was {BRIGHT + str(rnd_r) + RESET}")
            if guess == rnd_r:
                print(GREEN + f"Congratulation, you earned {BRIGHT}10{RESET}{GREEN} points!" + RESET)
                self.points += 10
            elif (rnd_r - 0.02) <= guess <= (rnd_r + 0.02):
                print(GREEN + f"Congratulation, you earned {BRIGHT}5{RESET}{GREEN} points!" + RESET)
                self.points += 5
            elif (rnd_r - 0.05) <= guess <= (rnd_r + 0.05):
                print(GREEN + f"Congratulation, you earned {BRIGHT}2{RESET}{GREEN} points!" + RESET)
                self.points += 2
            elif (rnd_r - 0.1) <= guess <= (rnd_r + 0.1):
                print(GREEN + f"Congratulation, you earned {BRIGHT}1{RESET}{GREEN} point!" + RESET)
                self.points += 1
            else:
                print(RED + f"Oh no! you lost {BRIGHT}1{RESET + RED} health point!" + RESET)
                self.health -= 1

            if self.health == 0:
                self.playing = False
                print(f"{RED}You lost all your health points!{RESET}")
                print(f"You earned {GREEN + str(self.points) + RESET} points in total. Congratulation!")
                input("[Press Enter to play again]")
                self.history.append(self.points)
                self.points = 0
                self.health = 3
                self.playing = True
                plt.close()
            else:
                print(f"Score: {GREEN+str(self.points)+RESET}")
                print(f"Health: {RED+str(self.health)}/3"+RESET)
                input(f"{BRIGHT}Next plot?{RESET} [press enter]")
                plt.close()


print(f"{RED + get_banner(version) + RESET}")
print(f"Welcome to {BRIGHT}Guess The Correlation{RESET}!")
print(f"{color.Style.DIM}developed by Anton Hauffe, inspired by https://www.guessthecorrelation.com/ {RESET}")
print(f"{BRIGHT + get_banner('Tutorial') + RESET}")
print("-> Wait until the scatterplot appears")
print("-> I recommend to drag the console window to the right of your screen since the appearing plot could "
      "eventually cover the console.")
print("-> Furthermore, you have to click at the console after a plot was drawn or a new round was started")
print("-> guess the correlation coefficient between 0 and 1")
print(f"-> if you are close, (+-0.1) you get {GREEN}1{RESET} point")
print(f"-> if you are closer, (+-0.05) you get {GREEN}2{RESET} points")
print(f"-> if you very close, (+-0.02) you get {GREEN}5{RESET} points")
print(f"-> if you are exact, you get {BRIGHT + GREEN}10{RESET} points")
print(f"-> if you missed, you lose {RED}1 of 3{RESET} health points")
print(f"{BRIGHT + GREEN}Good Luck!{RESET}")
print(f"{BRIGHT + get_banner('Tutorial End') + RESET}")
input("[Press Enter to start the game]")
username = input("Enter your name:")
game = Game(username)
