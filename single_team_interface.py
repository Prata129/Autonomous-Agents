import argparse

from grid import Grid
from interface import Interface
from observation import Observation
from robots.greedy_robot import GreedyRobot
from robots.random_robot import RandomRobot
from robots.rational_robot import QLearningRobot
from robots.role_robot import RoleRobot


def main(width, height, choice, uncertainty):
    if choice == 1:
        robot_types = [QLearningRobot, QLearningRobot,
                       QLearningRobot, QLearningRobot]
    elif choice == 2:
        robot_types = [RoleRobot, RoleRobot, RoleRobot, RoleRobot]
    elif choice == 3:
        robot_types = [GreedyRobot, GreedyRobot, GreedyRobot, GreedyRobot]
    else:
        robot_types = [RandomRobot, RandomRobot, GreedyRobot, GreedyRobot]

    grid = Grid((width, height), robot_types, uncertainty)

    # initial observations
    observation = Observation(grid,
                              grid.get_size(),
                              grid.get_robots(),
                              grid.get_trash())
    for robot in grid.get_robots():
        robot.see(observation)

    interface = Interface(grid)
    interface.game_loop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--width", type=int, default=9)
    parser.add_argument("--height", type=int, default=9)
    parser.add_argument("--choice", type=int, default=1)
    parser.add_argument("--uncertainty", type=int, default=0)
    opt = parser.parse_args()
    main(opt.width, opt.height, opt.choice, opt.uncertainty)
