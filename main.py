import pygame
import math
from create_maze import create_maze_animation
from particle import Particle
from object import Object
from maze_default import maze

WIDTH = 1200
HEIGHT = 400
OBJ_NUMBER = 3

sentences = {
    0: "You find yourself in the Backrooms...",
    1: "An endless maze of yellowed walls and buzzing lights.",
    2: "The air is thick with unease, and the silence presses down on you.",
    3: f"\"You must find the {OBJ_NUMBER} to espace this space, quick ! Before they find you\"",
    4: "\"Perfect ! You finally made it ! Thanks for the help ! Good luck for the rest !\"",
}


def createObjects(number: int) -> list[Object]:
    objects = []
    for _ in range(number):
        objects.append(Object())
    return objects


def drawText(surface: pygame.Surface, font: pygame.font.Font, sentence: str):
    text = font.render(sentence, True, "grey100")
    surface.blit(text, (0, 0))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill((20, 20, 20))
    # create_maze_animation(WIDTH, HEIGHT, screen, bg, clock, 50)
    ceiling = pygame.Surface((WIDTH // 2, HEIGHT // 2))
    ceiling.fill((87, 82, 73))
    floor = pygame.Surface((WIDTH // 2, HEIGHT // 2))
    floor.fill((113, 82, 41))

    wall_texture = pygame.image.load("wallpaper.png").convert()
    wall_texture = pygame.transform.scale(wall_texture, (400, 100))
    text_font = pygame.font.SysFont("Consolas", 24, bold=True)
    objects = createObjects(OBJ_NUMBER)
    remaining_obj = OBJ_NUMBER
    player = Particle((20, 20), 500)

    LEFT, RIGHT, FORWARD, REVERSE = False, False, False, False
    game_started = False
    game_finished = False
    story = 0
    while not game_started:
        screen.fill("black")
        drawText(screen, text_font, sentences[story])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen.fill("black")
                    drawText(screen, text_font, sentences[story])
                    pygame.display.update()
                    story += 1
                    if story == sentences.__len__() - 1:
                        game_started = True
    while True:
        if not objects and not game_finished:
            screen.fill("black")
            drawText(screen, text_font, sentences[story])
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    LEFT = True
                if event.key == pygame.K_RIGHT:
                    RIGHT = True
                if event.key == pygame.K_UP:
                    FORWARD = True
                if event.key == pygame.K_DOWN:
                    REVERSE = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_SPACE and not objects and not game_finished:
                        game_finished = True
                        player.pos = (20, 20)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    LEFT = False
                if event.key == pygame.K_RIGHT:
                    RIGHT = False
                if event.key == pygame.K_UP:
                    FORWARD = False
                if event.key == pygame.K_DOWN:
                    REVERSE = False

        # Updating the particle position and direction based on user input.
        new_pos = player.pos
        if LEFT:
            player.dir -= 20
        if RIGHT:
            player.dir += 20
        if FORWARD:
            angle = math.radians(player.dir / 10)
            x = player.pos[0] + (1 * math.cos(angle))
            y = player.pos[1] + (1 * math.sin(angle))
            new_pos = (x, y)
        if REVERSE:
            angle = math.radians(player.dir / 10)
            x = player.pos[0] - (1 * math.cos(angle))
            y = player.pos[1] - (1 * math.sin(angle))
            new_pos = (x, y)
        player.update(new_pos, maze)

        # Displaying background, rays, walls and the particle.
        screen.blit(bg, (0, 0))
        screen.blit(ceiling, (WIDTH // 2, 0))
        screen.blit(floor, (WIDTH // 2, HEIGHT // 2))
        for ray in player.rays:
            pygame.draw.aaline(screen, (240, 240, 240), ray.pos, ray.terminus, 1)
        for wall in maze:
            pygame.draw.line(screen, (200, 200, 200), wall[0], wall[1], 1)
        pygame.draw.circle(screen, (100, 255, 100), player.pos, 7)
        for obj in objects:
            obj.draw(screen)
            if math.floor(player.pos[0]) == obj.pos[0] and math.floor(player.pos[1]) == obj.pos[1]:
                objects.remove(obj)
                remaining_obj -= 1

        slice_w = (WIDTH // 2) / len(player.rays)
        offset = WIDTH // 2
        for i, ray in enumerate(player.rays):
            if ray.active_wall:
                if ray.terminus[0] == ray.active_wall[0][0]:
                    img_start = abs(ray.terminus[1] - ray.active_wall[0][1]) * 10
                else:
                    img_start = abs(ray.terminus[0] - ray.active_wall[0][0]) * 10
                if img_start >= 300:
                    img_start -= 300
                h = (10 / ray.corrected_distance) * HEIGHT
                if h > HEIGHT:
                    h = HEIGHT
                w = h * 4
                y = (HEIGHT / 2) - (h / 2)
                img_start = (img_start * w) / 400
                tmp_img = pygame.transform.scale(wall_texture, (w, h))
                screen.blit(
                    tmp_img, (offset + (i * slice_w), y), (img_start, 0, slice_w, h)
                )

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
