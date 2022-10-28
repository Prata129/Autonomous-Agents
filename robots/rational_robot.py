from collections import defaultdict

import numpy

from robots.robot import Robot

N_ACTIONS = 5
DOWN, LEFT, UP, RIGHT, STAY = range(N_ACTIONS)
ACTIONS = (DOWN, LEFT, UP, RIGHT)


class QLearningRobot(Robot):

    def __init__(self, position, uncertainty, learning_rate=0.3, discount_factor=0.99, exploration_rate=0.15, initial_q_values=0.0):
        self._Q = defaultdict(lambda: numpy.ones(N_ACTIONS) * initial_q_values)
        self._learning_rate = learning_rate
        self._discount_factor = discount_factor
        self._exploration_rate = exploration_rate
        super().__init__("Q-Learning Robot", position, uncertainty)

    def setup_environments(self, train_environment, eval_environment):
        self._train_environment = train_environment
        self._eval_environment = eval_environment

    def get_Q(self):
        return self._Q

    def set_Q(self, Q):
        self._Q = Q

    def action(self):

        x = (self._position, tuple(self._observation.get_trash()))
        # Access Q-Values for current observation
        q_values = self._Q[x]

        if not self._training or (self._training and numpy.random.uniform(0, 1) > self._exploration_rate):
            # Exploit
            actions = numpy.argwhere(
                q_values == numpy.max(q_values)).reshape(-1)
        else:
            # Explore
            actions = range(N_ACTIONS)

        return numpy.random.choice(actions)

    def next(self, action, next_observation, reward):

        x, a, r, y = (self._position, tuple(self._observation.get_trash())
                      ), action, reward, next_observation
        alpha, gamma = self._learning_rate, self._discount_factor

        Q_xa, Q_y = self._Q[x][a], self._Q[y]
        max_Q_ya = max(Q_y)

        # Update rule for Q-Learning
        self._Q[x][a] = Q_xa + alpha * (r + gamma*max_Q_ya - Q_xa)
