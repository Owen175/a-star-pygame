import pygame
import time


class Pathfinding:
    def __init__(self, pause: float = 0.0):
        self.pause = pause
        self.grid_x, self.grid_y = 10, 10
        self.tile_size = 90
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
                    if [x, y] in locations:
                        locations.remove([x, y])
                        self.colour_tile(self.BLACK, x, y, update=True)
                    else:
                        locations.append([x, y])
                        self.colour_tile(self.GRAY, x, y, update=True)
                if event.type == pygame.WINDOWCLOSE:
                    exit()
        return locations

    def draw_grid(self) -> None:
        self.screen.fill(self.WHITE)
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                self.colour_tile(self.BLACK, x, y)
        pygame.display.flip()

    def colour_tile(self, colour: tuple[int, int, int], x: int, y: int, update: bool = False) -> None:
        rect = pygame.Rect(x * self.tile_size + 1, y * self.tile_size + 1, self.tile_size - 2,
                           self.tile_size - 2)
        pygame.draw.rect(self.screen, colour, rect)
        if update:
            pygame.display.update((x * self.tile_size + 1, y * self.tile_size + 1),
                                  (self.tile_size - 2, self.tile_size - 2))

    def update_stack(self, stack: list[list[int]], parent_dict: dict, px: int, py: int, x: int, y: int) \
            -> list[list[int]]:
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
        return stack

    def insert_(self, hg_list: list[list[int | list[int]]], point_hg: int, temp_x: int, temp_y: int, x: int, y: int,
                g: int) -> list[list[int | list[int]]]:
        if len(hg_list) == 0:
            return [[temp_x, temp_y, [point_hg, g], x, y]]
        ls = hg_list[:]
        if ls[-1][2][0] < point_hg:
            ls.append([temp_x, temp_y, [point_hg, g], x, y])
        else:
            for i, (_, _, [list_hg, _], _, _) in enumerate(ls):
                if list_hg >= point_hg:
                    ls.insert(i, [temp_x, temp_y, [point_hg, g], x, y])
                    break
        return ls
    def pathfind(self, start_point: list[int], end_point: list[int]) -> None:
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
                time.sleep(self.pause)
            old_stack = stack[:]
            # is double-checking when there is no path
            print(hg_list[0])
            temp = hg_list.pop(0)
            x, y, _, px, py = temp
            # except:
            #     print(temp)
            hg, g = _
            stack = self.update_stack(stack, parent_dict, px, py, x, y)

            if [x, y] == end_point:
                game_end = True
                break
            for temp_x, temp_y in self.get_unchecked_neighbours(x, y, checked_list, hg_list):
                point_hg = self.evaluate_point(temp_x, temp_y, g + 1, end_point)[0]
                hg_list = self.insert_(hg_list, point_hg, temp_x, temp_y, x, y, g + 1)
                parent_dict[(temp_x, temp_y)] = (x, y)
                self.colour_tile(self.BLUE, temp_x, temp_y)

            checked_list.append([x, y])
            self.colour_tile(self.RED, x, y)
            self.draw_stack(stack, old_stack)
            pygame.display.flip()

        if game_end:
            print('Got there')
            self.colour_tile(self.PURPLE, end_point[0], end_point[1])
            for x, y in stack[:-1]:
                self.colour_tile(self.GREEN, x, y)
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
            self.colour_tile(self.RED, x, y)
        for x, y in stack_changes:
            self.colour_tile(self.GREEN, x, y)

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
