import random

from robots.robot import Robot

N_ACTIONS = 5


class RandomRobot(Robot):
    def __init__(self, position, uncertainty) -> None:
        super().__init__("Random Robot", position, uncertainty)

    def action(self):
        return random.randint(0, N_ACTIONS - 1)
