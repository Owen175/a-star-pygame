import pygame
import time


class Pathfinding:
    def __init__(self, pause: float = 0.0):
        self.pause = pause
        self.grid_x, self.grid_y = 60, 60
        self.tile_size = 15
        self.screen_size = self.grid_x * self.tile_size, self.grid_y * self.tile_size
        # To be added to the checked_locations list
        pygame.init()
        pygame.display.set_caption('A Star Pathfinding')
        self.screen = pygame.display.set_mode(self.screen_size)
        self.WHITE, self.BLACK, self.GREEN, self.RED, self.BLUE, self.PURPLE, self.GRAY = (200, 200, 200), (0, 0, 0), \
            (0, 200, 0), (200, 0, 0), (0, 0, 200), (100, 0, 100), (100, 100, 100)
        self.draw_grid()
        self.obstacle_locations = self.get_obstacle_locations()

    def get_obstacle_locations(self) -> list[list[int]]:
        locations = []
        cont = True
        while cont:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        cont = False
                        break
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    x, y = x // self.tile_size, y // self.tile_size
                    rect = pygame.Rect(x * self.tile_size + 1, y * self.tile_size + 1, self.tile_size - 2,
                                       self.tile_size - 2)
                    if [x, y] in locations:
                        locations.remove([x, y])
                        pygame.draw.rect(self.screen, (0, 0, 0), rect)
                    else:
                        locations.append([x, y])
                        pygame.draw.rect(self.screen, self.GRAY, rect)
                    pygame.display.flip()
                if event.type == pygame.WINDOWCLOSE:
                    exit()
        return locations

    def draw_grid(self) -> None:
        self.screen.fill(self.WHITE)
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                rect = pygame.Rect(x * self.tile_size + 1, y * self.tile_size + 1, self.tile_size - 2,
                                   self.tile_size - 2)
                pygame.draw.rect(self.screen, self.BLACK, rect)
        pygame.display.flip()

    def colour_tile(self, colour: tuple[int], x: int, y: int, update: bool = False) -> None:
        rect = pygame.Rect(x * self.tile_size + 1, y * self.tile_size + 1, self.tile_size - 2,
                           self.tile_size - 2)
        pygame.draw.rect(self.screen, colour, rect)
        if update:
            pygame.display.update((x * self.tile_size + 1, y * self.tile_size + 1),
                                  (self.tile_size - 2, self.tile_size - 2))

    def pathfind(self, start_point: list[int], end_point: list[int], pause: float = 0) -> None:
        # lowest h(n) + g(n) - insert into sorted list and always pick the least to explore tiles around
        # Store g with each value, so that it can be incremented and evaluated
        # need to append the point to an explored list also
        parent_dict = {}
        stack = [start_point]
        checked_list = self.obstacle_locations[:]
        checked_list.append(start_point)
        hg_list = [[x, y, self.evaluate_point(x, y, 1, end_point), start_point[0], start_point[1]] for x, y in
                   self.get_unchecked_neighbours(start_point[0], start_point[1], checked_list, [])]
        for x, y, _, px, py in hg_list:
            parent_dict[(x, y)] = (px, py)
        hg_list.sort(key=lambda a: a[2][0])
        game_end = False
        while len(hg_list) != 0:
            if self.pause:
                time.sleep(pause)
            old_stack = stack[:]
            # is double checking when there is no path
            x, y, _, px, py = hg_list.pop(0)
            hg, g = _
            if [px, py] == stack[-1]:
                stack.append([x, y])
            elif [px, py] in stack:
                stack = stack[:stack.index([px, py]) + 1]
                stack.append([x, y])
            else:
                appending = [(x, y), (px, py)]
                ppx, ppy = parent_dict[(px, py)]
                while [ppx, ppy] not in stack:
                    appending.append([ppx, ppy])
                    ppx, ppy = parent_dict[(ppx, ppy)]
                stack = stack[:stack.index([ppx, ppy]) + 1]
                appending.reverse()
                stack.extend(appending)

            if [x, y] == end_point:
                game_end = True
                break
            for temp_x, temp_y in self.get_unchecked_neighbours(x, y, checked_list, hg_list):
                point_hg = self.evaluate_point(temp_x, temp_y, g + 1, end_point)[0]
                if len(hg_list) == 0:
                    hg_list.append([temp_x, temp_y, [point_hg, g + 1], x, y])
                elif hg_list[-1][2][0] < point_hg:
                    hg_list.append([temp_x, temp_y, [point_hg, g + 1], x, y])
                else:
                    for i, (_, _, [list_hg, _], _, _) in enumerate(hg_list):
                        if list_hg >= point_hg:
                            hg_list.insert(i, [temp_x, temp_y, [point_hg, g + 1], x, y])
                            break
                parent_dict[(temp_x, temp_y)] = (x, y)
                rect = pygame.Rect(temp_x * self.tile_size + 1, temp_y * self.tile_size + 1, self.tile_size - 2,
                                   self.tile_size - 2)
                pygame.draw.rect(self.screen, self.BLUE, rect)
                pygame.display.flip()

            checked_list.append([x, y])
            rect = pygame.Rect(x * self.tile_size + 1, y * self.tile_size + 1, self.tile_size - 2, self.tile_size - 2)
            pygame.draw.rect(self.screen, self.RED, rect)
            self.draw_stack(stack, old_stack)
            pygame.display.flip()

        if game_end:
            print('Got there')
            rect = pygame.Rect(end_point[0] * self.tile_size + 1, end_point[1] * self.tile_size + 1, self.tile_size - 2,
                               self.tile_size - 2)
            pygame.draw.rect(self.screen, self.PURPLE, rect)
            for x, y in stack[:-1]:
                rect = pygame.Rect(x * self.tile_size + 1, y * self.tile_size + 1, self.tile_size - 2,
                                   self.tile_size - 2)
                pygame.draw.rect(self.screen, self.GREEN, rect)
            pygame.display.flip()
        else:
            print('Not possible')

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.WINDOWCLOSE:
                    exit()

    def draw_stack(self, stack: list[list[int]], old_stack: list[list[int]]) -> None:
        c = 0
        while stack[:c + 1] == old_stack[:c + 1]:
            c += 1

        stack_changes = stack[c:]
        old_stack_changes = old_stack[c:]
        for x, y in old_stack_changes:
            rect = pygame.Rect(x * self.tile_size + 1, y * self.tile_size + 1, self.tile_size - 2,
                               self.tile_size - 2)
            pygame.draw.rect(self.screen, self.RED, rect)
        for x, y in stack_changes:
            rect = pygame.Rect(x * self.tile_size + 1, y * self.tile_size + 1, self.tile_size - 2, self.tile_size - 2)
            pygame.draw.rect(self.screen, self.GREEN, rect)

    def get_unchecked_neighbours(self, x: int, y: int, checked_list: list[list[int]], hg_list) -> list[list[int]]:
        neighbours = []
        # checks if in the checked / to be checked list
        if x > 0:
            neighbours.append([x - 1, y])
        if y > 0:
            neighbours.append([x, y - 1])
        if y < self.grid_y - 1:
            neighbours.append([x, y + 1])
        if x < self.grid_x - 1:
            neighbours.append([x + 1, y])

        to_be_checked = [[x, y] for x, y, *_ in hg_list]
        return [[x, y] for x, y in neighbours if [x, y] not in to_be_checked and [x, y] not in checked_list]

    def evaluate_point(self, x: int, y: int, g: int, end_point: list[int]) -> list[int]:
        return [self.h(x, y, end_point) + g, g]

    @staticmethod
    def h(x: int, y: int, end_point: list[int]) -> int:
        return abs(x - end_point[0]) + abs(y - end_point[1])
        # Manhattan distance

if __name__ == '__main__':
    p = Pathfinding()
    p.pathfind([0, 0], [p.grid_x - 1, p.grid_y - 1])
