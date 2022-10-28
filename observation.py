class Observation:
    def __init__(self, grid, size, robots, trash):
        self._grid = grid
        self._size = size
        self._robots = robots
        self._trash = trash

    def get_size(self):
        return self._size

    def get_robots(self):
        return self._robots

    def get_trash(self):
        return self._trash

    def is_trash(self, pos):
        return pos in self._trash

    def simulate_move(self, curr_pos, action):
        return self._grid.simulate_move(curr_pos, action)
