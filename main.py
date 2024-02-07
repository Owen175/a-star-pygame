import pygame


class Pathfinding:
    def __init__(self):
        self.grid_x, self.grid_y = 15, 15
        self.tile_size = 60
        self.screen_size = self.grid_x * self.tile_size, self.grid_y * self.tile_size
        self.obstacle_locations = []
        # To be added to the checked_locations list
        pygame.init()
        pygame.display.set_caption('A Star Pathfinding')
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_grid(self):
        pass

    def pathfind(self, start_point, end_point):
        # lowest h(n) + g(n) - insert into sorted list and always pick the least to explore tiles around
        # Store g with each value, so that it can be incremented and evaluated
        # need to append the point to an explored list also
        checked_list = [start_point]
        hg_list = [[x, y, self.evaluate_point(x, y, 1, end_point)] for x, y in
                   self.get_unchecked_neighbours(start_point[0], start_point[1], checked_list)]
        hg_list.sort(key=lambda a: a[2][0])
        game_end = False
        while len(hg_list) != 0:
            x, y, _ = hg_list.pop(0)
            hg, g = _

            if [x, y] == end_point:
                game_end = True
                break
            for x, y in self.get_unchecked_neighbours(x, y, checked_list):
                print(x, y)
                point_hg = self.evaluate_point(x, y, g + 1, end_point)[0]
                print(hg_list[-1])
                if hg_list[-1][2][0] < point_hg:
                    hg_list.append([x, y, [point_hg, g + 1]])
                else:
                    for i, (_, _, [list_hg, _]) in enumerate(hg_list):
                        if list_hg >= point_hg:
                            hg_list.insert(i, [x, y, [point_hg, g + 1]])


            checked_list.append([x, y])


        if game_end:
            print('Got there')
        else:
            print('Not possible')
    def get_unchecked_neighbours(self, x, y, checked_list):
        neighbours = []

        if x > 0:
            if [x - 1, y] not in checked_list:
                neighbours.append([x - 1, y])
            if y > 0:
                if [x - 1, y - 1] not in checked_list:
                    neighbours.append([x - 1, y - 1])
            if y < self.grid_y - 1:
                if [x - 1, y + 1] not in checked_list:
                    neighbours.append([x - 1, y + 1])
        if y > 0:
            if [x, y - 1] not in checked_list:
                neighbours.append([x, y - 1])
        if y < self.grid_y - 1:
            if [x, y + 1] not in checked_list:
                neighbours.append([x, y + 1])
        if x < self.grid_x - 1:
            if [x + 1, y] not in checked_list:
                neighbours.append([x + 1, y])
            if y > 0:
                if [x + 1, y - 1] not in checked_list:
                    neighbours.append([x + 1, y - 1])
            if y < self.grid_y - 1:
                if [x + 1, y + 1] not in checked_list:
                    neighbours.append([x + 1, y + 1])
        return neighbours

    def evaluate_point(self, x, y, g, end_point):
        return [self.h(x, y, end_point) + g, g]

    @staticmethod
    def h(x, y, end_point):
        return abs(x - end_point[0]) + abs(y - end_point[1])
        # Manhattan distance


p = Pathfinding()
p.pathfind([0, 0], [14, 14])
