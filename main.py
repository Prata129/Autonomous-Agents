import argparse

import numpy as np

from grid import Grid
from observation import Observation
from robots.greedy_robot import GreedyRobot
from robots.random_robot import RandomRobot
from robots.rational_robot import QLearningRobot
from robots.role_robot import RoleRobot
from utils import compare_results, compare_results_learning

RENDER = False


def train_eval_loop_multi(size, n_evaluations, robot_types, uncertainty, n_training_episodes, n_eval_episodes):
    print(f"Train-Eval Loop for QLearning Team")
    results = np.zeros((n_evaluations, n_eval_episodes))

    train_grid = Grid(size, robot_types, uncertainty)

    eval_grid = Grid(size, robot_types, uncertainty)

    for evaluation in range(n_evaluations):
        print(f'Running evaluation {evaluation + 1} / {n_evaluations}')
        # Train
        run_team(train_grid, n_training_episodes, training=True)

        train_robots = train_grid.get_robots()
        eval_robots = eval_grid.get_robots()
        for i in range(len(train_robots)):
            q = train_robots[i].get_Q()
            eval_robots[i].set_Q(q)

        # Eval
        results[evaluation] = run_team(eval_grid, n_eval_episodes)
    return results


def run_team(grid, n_episodes, training=False):
    results_team = np.zeros(n_episodes)

    for episode in range(n_episodes):

        if episode % 10 == 0:
            print(f'Running episode {episode + 1} / {n_episodes}')

        max_steps = 500

        if not training and RENDER:
            grid.render()

        steps = 0

        while len(grid.get_trash()) != 0 and steps < max_steps:
            # update observations
            for robot in grid.get_robots():
                if training:
                    robot.train()
                else:
                    robot.eval()
                observation = Observation(grid,
                                          grid.get_size(),
                                          grid.get_robots(),
                                          grid.get_trash())
                robot.see(observation)

            grid.step(training)
            steps += 1

            if not training and RENDER:
                grid.render()

        results_team[episode] = steps

        # reset the grid after each episode
        grid.reset()

    return results_team


def main(n_episodes, size, uncertainty, render, n_training_episodes, n_eval_episodes, n_evaluations):
    global RENDER
    RENDER = render
    results = {}
    teams = {'Random Team': [RandomRobot, RandomRobot, RandomRobot, RandomRobot],
             'Learning Team': [QLearningRobot, QLearningRobot, QLearningRobot, QLearningRobot],
             'Greedy Role': [RoleRobot, RoleRobot, RoleRobot, RoleRobot],
             'Greedy Team': [GreedyRobot, GreedyRobot, GreedyRobot, GreedyRobot],
             '2 Random +\n 2 Greedy': [RandomRobot, RandomRobot, GreedyRobot, GreedyRobot], }

    for team in teams:
        print(f'Running {team}')
        if team == 'Learning Team':
            results[team] = train_eval_loop_multi(
                size, n_evaluations, teams[team], uncertainty, n_training_episodes, n_eval_episodes)
        else:
            grid = Grid(size, teams[team], uncertainty)
            results[team] = run_team(grid, n_episodes)

    compare_results(
        results,
        title="Teams Comparison on 'Multi Agent Cooperative Grid Sweep'",
        colors=["blue", "green", "orange", "red", "purple"]
    )

    compare_results_learning(
        {'Learning Team': results['Learning Team']}, title="Learning Team", colors=["blue"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--width", type=int, default=9)
    parser.add_argument("--height", type=int, default=9)
    parser.add_argument("--uncertainty", type=float, default=0.0)
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--episodes_per_training", type=int, default=100)
    parser.add_argument("--episodes_per_evaluation", type=int, default=64)
    parser.add_argument("--evaluations", type=int, default=10)
    opt = parser.parse_args()
    main(opt.episodes, (opt.height, opt.width), opt.uncertainty,
         opt.render, opt.episodes_per_training, opt.episodes_per_evaluation, opt.evaluations)
