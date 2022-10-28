import random

import numpy

from robots.robot import Robot

N_ACTIONS = 5
DOWN, LEFT, UP, RIGHT, STAY = range(N_ACTIONS)
ACTIONS = (DOWN, LEFT, UP, RIGHT)


class RoleRobot(Robot):

    def __init__(self, position, uncertainty):
        super().__init__("Role Robot", position, uncertainty)
        self._roles = None
        self._curr_role = None

    def potential_function(self, robot_pos, role):
        if robot_pos[0] >= role[0] and robot_pos[0] <= role[1]:
            return 0
        else:
            return -abs(role[1] - robot_pos[0])

    def role_assignment(self):
        # create roles
        if self._roles is None:
            self._roles = []
            height = self._observation.get_size()[0]
            n_zones = len(self._observation.get_robots())
            step = height // n_zones  # 11/5 = 2.2
            remainder = height % n_zones
            if remainder != 0:
                if remainder / n_zones >= 0.5:
                    step += 1
            zone = (0, step - 1)
            self._roles.append(zone)
            for _ in range(n_zones - 1):
                zone = (zone[1] + 1, zone[1] + 1 + step - 1)
                self._roles.append(zone)
            # update upper bound of last zone to include the whole grid
            self._roles[-1] = (self._roles[-1][0],
                               self._observation.get_size()[0] - 1)

        # calculate potencials
        r_positions = []
        potentials = {}
        for robot in self._observation.get_robots():

            robot_pos = robot.get_position()
            r_positions.append(robot_pos)
            aux = []
            for role in self._roles:
                aux.append(self.potential_function(
                    robot_pos, role))
            potentials[robot_pos] = aux

        # pick roles
        roles = {}
        for robot_pos, agent_potentials in potentials.items():
            role_index = agent_potentials.index(max(agent_potentials))
            role = self._roles[role_index]
            while role in roles.values():
                agent_potentials[role_index] = min(agent_potentials) - 1
                role_index = agent_potentials.index(max(agent_potentials))
                role = self._roles[role_index]
            roles[robot_pos] = role

        return roles

    def action(self) -> int:

        # Compute potential-based role assignment every `role_assign_period` steps.
        if self._curr_role is None:
            role_assignments = self.role_assignment()
            self._curr_role = role_assignments[self.get_position()]

        trash = self._observation.get_trash()
        if len(trash) == 0:
            # simulation will end
            return STAY

        # if the robot is already in its role zone
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
                    if observation.is_trash(neighbour) and (neighbour[0] >= self._curr_role[0] and neighbour[0] <= self._curr_role[1]):
                        return new_path

                # mark position as explored
                explored.append(pos)

        # in case there's no path between the 2 positions
        return [start]
