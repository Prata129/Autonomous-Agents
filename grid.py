import random
from itertools import product

from interface import Interface


class Grid:
    def __init__(self, size, robot_types, uncertainty=0):
        self._size = size
        self._robot_types = robot_types
        self._uncertainty = uncertainty

        self._interface = None

        free_pos = \
            [(x, y) for x, y in product(range(size[0]), range(size[1]))]

        # create robots
        self._robots = []
        for robot_type in robot_types:
            pos = random.choice(free_pos)
            free_pos.remove(pos)
            self._robots.append(robot_type(pos, uncertainty))

        robot_positions = set([r.get_position() for r in self._robots])

        # create trash
        trash = [(i, j) for i, j in product(range(size[0]), range(size[1]))]
        trash = set(trash)

        # create obstacles
        obstacles = []
        # all even positions get an obstacle
        for (i, j) in product(range(size[0]), range(size[1])):
            if i % 2 == 0 and j % 2 == 0:
                obstacles.append((i, j))

        obstacles = set(obstacles)

        # remove overlaping entities
        obstacles = obstacles - robot_positions
        trash = trash - robot_positions - obstacles

        self._trash = trash
        self._obstacles = obstacles

    def reset(self):
        self.__init__(self._size, self._robot_types, self._uncertainty)

    def get_size(self):
        return self._size

    def get_robots(self):
        return self._robots

    def get_trash(self):
        return self._trash

    def get_obstacles(self):
        return self._obstacles

    def step(self, training=False):
        for robot in self._robots:
            action = robot.action()
            reward = self.__update_robot_position(robot, action)
            if training:
                next_pos = self.simulate_move(robot.get_position(), action)
                robot.next(action, (next_pos, tuple(self._trash)), reward)

    def is_trash(self, pos):
        return pos in self._trash

    def __is_valid(self, pos):
        return (0 <= pos[0] < self._size[0]) and (0 <= pos[1] < self._size[1])

    def __is_cell_vacant(self, pos):
        if not self.__is_valid(pos):
            return False
        if pos in self._obstacles:
            # can't move into an obstacle
            return False
        for robot in self._robots:
            if robot.get_position() == pos:
                return False

        return True

    def simulate_move(self, curr_pos, action):
        next_pos = None
        if action == 0:  # down
            next_pos = (curr_pos[0] + 1, curr_pos[1])
        elif action == 1:  # left
            next_pos = (curr_pos[0], curr_pos[1] - 1)
        elif action == 2:  # up
            next_pos = (curr_pos[0] - 1, curr_pos[1])
        elif action == 3:  # right
            next_pos = (curr_pos[0], curr_pos[1] + 1)
        elif action == 4:  # no-op
            next_pos = None
        else:
            raise Exception('Action Not found!')

        if next_pos is not None and self.__is_cell_vacant(next_pos):
            return next_pos
        else:
            return curr_pos

    def __update_robot_position(self, robot, action):
        curr_pos = robot.get_position()
        robot.set_position(self.simulate_move(curr_pos, action))

        # remove trash
        reward = -1
        to_remove = []
        for trash in self._trash:
            if trash == robot.get_position():
                to_remove.append(trash)
                reward = 1
        for trash in to_remove:
            self._trash.remove(trash)
        return reward

    def __str__(self):
        grid = ''
        for i in range(self._size[0]):
            grid_line = ''
            for j in range(self._size[1]):
                skip = False
                for robot in self._robots:
                    if robot.get_position() == (i, j):
                        grid_line += str(robot.get_id()) + ' '
                        skip = True
                        break
                if skip:
                    continue

                for trash in self._trash:
                    if trash == (i, j):
                        grid_line += 't '
                        skip = True
                        break
                if skip:
                    continue

                for obstacle in self._obstacles:
                    if obstacle == (i, j):
                        grid_line += 'o '
                        skip = True
                        break
                if skip:
                    continue

                grid_line += '_ '
            grid += grid_line + '\n'

        return grid

    def render(self):
        if self._interface is None:
            self._interface = Interface(self)
        self._interface.render()
