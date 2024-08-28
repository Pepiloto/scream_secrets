import pygame
from maze_builder import create_grid
from random import randint


def create_maze_animation(
    width: int,
    height: int,
    screen: pygame.Surface,
    bg: pygame.Surface,
    clock: pygame.time.Clock,
    speed: int = 15,
):
    grid = create_grid(width, height, 40)
    stack = [grid[0]]
    path = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # Displaying the background surface.
        screen.blit(bg, (0, 0))
        # Algorithm...
        if stack:
            current = stack.pop()
            current.visited = True
            viable_neighbours = []
            for neighbour in current.neighbours:
                if not neighbour.visited:
                    viable_neighbours.append(neighbour)
            if viable_neighbours:
                select = randint(0, len(viable_neighbours) - 1)
                stack.append(viable_neighbours[select])
                current.remove_shared_wall(viable_neighbours[select])
                path.append(current)
            else:
                if path:
                    backstep = path.pop()
                    stack.append(backstep)
            # Displaying the position of the current cell/block.
            position = (current.pos[0] + 20, current.pos[1] + 20)
            pygame.draw.circle(screen, (255, 255, 100), position, 12)
        # Displaying the maze walls as they are constructed.
        for cell in grid:
            if cell.visited:
                for wall in cell.walls:
                    pygame.draw.line(screen, (200, 200, 200), wall[0], wall[1], 2)
        pygame.display.update()
        clock.tick(speed)
        if not stack:
            print("Maze created !")
            for i in range(grid.__len__()):
                print(f"{grid[i].pos} {grid[i].side}")
            return grid
