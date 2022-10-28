import random

import numpy

from robots.robot import Robot

N_ACTIONS = 5
DOWN, LEFT, UP, RIGHT, STAY = range(N_ACTIONS)
ACTIONS = (DOWN, LEFT, UP, RIGHT)


class GreedyRobot(Robot):
    def __init__(self, position, uncertainty) -> None:
        super().__init__("Greedy Robot", position, uncertainty)

    def action(self):
        trash = self._observation.get_trash()
        if len(trash) == 0:
            # simulation will end
            return STAY

        path = self.__path_to_closest_trash(self._observation, self._position)
        if len(path) == 1:
            return STAY

        direction = self.__direction_to_go(path[1])
        direction = numpy.random.choice([direction, STAY], p=[
            1-self.get_uncertainty(), self.get_uncertainty()])

        return direction

    def __close_horizontally(self, distances):
        if distances[1] > 0:
            return RIGHT
        elif distances[1] < 0:
            return LEFT
        else:
            return STAY

    def __close_vertically(self, distances):
        if distances[0] > 0:
            return DOWN
        elif distances[0] < 0:
            return UP
        else:
            return STAY

    def __direction_to_go(self, trash_position):
        distances = (trash_position[0] - self._position[0],
                     trash_position[1] - self._position[1])
        abs_distances = (abs(distances[0]), abs(distances[1]))
        if abs_distances[0] > abs_distances[1]:
            return self.__close_vertically(distances)
        elif abs_distances[0] < abs_distances[1]:
            return self.__close_horizontally(distances)
        else:
            roll = random.uniform(0, 1)
            return self.__close_horizontally(distances) if roll > 0.5 else self.__close_vertically(distances)

    def __path_to_closest_trash(self, observation, start):
        # keep track of explored positions
        explored = []
        # keep track of all the paths to be checked
        queue = [[start]]

        # return path if start is goal
        if observation.is_trash(start):
            return [start]

        # keeps looping until all possible paths have been checked
        while queue:
            # pop the first path from the queue
            path = queue.pop(0)
            # get the last position from the path
            pos = path[-1]
            if pos not in explored:
                actions = list(ACTIONS[:])
                random.shuffle(actions)
                neighbours = [observation.simulate_move(
                    pos, action) for action in ACTIONS]
                # go through all neighbour positions, construct a new path and
                # push it into the queue
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    # return path if neighbour is goal
                    if observation.is_trash(neighbour):
                        return new_path

                # mark position as explored
                explored.append(pos)

        # in case there's no path between the 2 positions
        return [start]
