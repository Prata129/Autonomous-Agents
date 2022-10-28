class Robot:

    _robot_id = 1

    def __init__(self, name, position, uncertainty):
        self._name = name
        self._observation = None
        self._uncertainty = uncertainty

        self._id = Robot._robot_id
        Robot._robot_id += 1

        self._position = position
        self._training = False

    def train(self):
        self._training = True

    def eval(self):
        self._training = False

    def see(self, observation):
        self._observation = observation

    def action(self) -> int:
        raise NotImplementedError()

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position

    def get_id(self):
        return self._id

    def get_uncertainty(self):
        return self._uncertainty
