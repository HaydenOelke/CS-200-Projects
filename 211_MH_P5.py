"""
Hayden Oelke 
CS 211 
2024 - 05 - 02
Credits: ChatGPT, Charlie Mayher
"""


import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class MH:
    def __init__(self, n_doors=3) -> None:
        self.n_doors = n_doors
        self.n_trials = 0 #the number of trials
        self.n_sw = 0 #the number of time the player switches doors
        self.sw_w_n = 0 #the number of times swwitching led to winning
        self.sw_w = [] #an array recording the frequency of winning after switching
        self.st_w_n = 0 #the number of times staying with the original door led to winning
        self.st_w = [] #an array recording the frequency of winning after staying with the original door for each trial

    def __str__(self) -> str:
        return (f"MH problem\n"
                f"  n_doors = {self.n_doors}\n"
                f"  n_trials = {self.n_trials}\n"
                f"  n_sw = {self.n_sw}\n"
                f"  sw_w_n = {self.sw_w_n}\n"
                f"  sw_w [{self.n_trials}] = {self.sw_w}...\n"
                f"  st_w_n = {self.st_w_n}\n"
                f"  st_w [{self.n_trials}] = {self.st_w}...")
    
    def trial(self, verbose=True):
        doors = [1, 2, 3]
        correct = random.choice(doors)  # Trial chooses correct door
        chosen = random.choice(doors)  # Trial chooses what door the player selects

        # Find the door to open that is not the chosen or the correct door
        # (Host opens a door revealing a goat)
        goat_doors = [door for door in doors if door not in {chosen, correct}]
        opened_door = random.choice(goat_doors) if len(goat_doors) > 1 else goat_doors[0]

        # Decide if the player switches
        switch = random.choice([False, True])
        switched_door = [door for door in doors if door not in {opened_door, chosen}][0]
        if switch:
            # Player switches to the remaining unopened door
            final_choice = switched_door
        else:
            # Player stays with the original choice
            final_choice = chosen
        
        self.update(switched_door, chosen, correct, switch)

        if verbose:
            print(f"correct = {correct}")
            print(f"chosen = {chosen}")
            print(f"switched_door = {switched_door}")
            print(f"n_trials = {self.n_trials}")
            print("switching doors" if switch else "not switching doors")
            print(f"no of times switching doors: {self.n_sw}")
            print(f"final choice: {final_choice}")
            print(f"freqs of switch and win: {self.sw_w}")
            print(f"freqs of stay and win: {self.st_w}")

    def update(self, switched_door, chosen, correct, switch):
        # Determine final choice based on whether the player switches
        final_choice = switched_door if switch else chosen
        win = (final_choice == correct)
        self.n_trials += 1

        if switch:
            self.n_sw += 1
            if win:
                self.sw_w_n += 1
            # Calculate win probability for switching
            current_freq = self.sw_w_n / self.n_sw
            self.sw_w.append(current_freq)
            # Append the last known stay win probability or 0 if none
            self.st_w.append(self.st_w[-1] if self.st_w else 0.0)
        else:
            if win:
                self.st_w_n += 1
            # Calculate win probability for staying
            current_freq = self.st_w_n / (self.n_trials - self.n_sw) if (self.n_trials - self.n_sw) else 0.0
            self.st_w.append(current_freq)
            # Append the last known switch win probability or 0 if none
            self.sw_w.append(self.sw_w[-1] if self.sw_w else 0.0)



    def experiment(self, nt=10):
        for _ in range(nt):
            self.trial()
            


    def animate_plot(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.n_trials)
        ax.set_ylim(0, 1)
        line1, = ax.plot([], [], 'r-', label='switch')
        line2, = ax.plot([], [], 'b-', label='no switch')
        ax.legend()
        ax.set_xlabel('N')
        ax.set_ylabel('prob')

        def update(frame):
            line1.set_data(range(frame + 1), self.sw_w[:frame + 1])
            line2.set_data(range(frame + 1), self.st_w[:frame + 1])
            return line1, line2
        ani = FuncAnimation(fig, update, frames=len(self.sw_w), repeat=False)
        plt.show()

    def plot(self):
        plt.figure(figsize=(10,5))
        plt.plot(self.sw_w, label = 'switch', color = 'red')
        plt.plot(self.st_w, label = 'Stayed',color = 'blue')
        plt.ylabel('prob')
        plt.xlabel('n')
        plt.show()



if __name__ == "__main__":
    random.seed(42)
    mh = MH()
    print(mh)

    # mh.trial()
    # print(mh)
    # mh.trial()
    # print(mh)
    # mh.trial()
    # print(mh)
    mh.experiment(1000)
    print(mh)

    mh.plot()

    mh.animate_plot()
