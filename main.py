import pygame, sys, random
import pygame.joystick
from pygame.math import Vector2

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.highest_score = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_highest_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (20, 20, 20)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = f'Score: {str(len(self.snake.body) - 3)}'
        score_surface = game_font.render(score_text, True, (255, 255, 255))
        score_x = int(cell_size * cell_number - 120)
        score_y = int(cell_size * cell_number + 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)

    def draw_highest_score(self):

        if int(len(self.snake.body) - 3) > self.highest_score:
            self.highest_score = len(self.snake.body) - 3
        hscore_text = f'Highest Score: {self.highest_score}'
        hscore_surface = game_font.render(hscore_text, True, (255, 255, 255))
        hscore_x = int(180)
        hscore_y = int(cell_size * cell_number + 40)
        hscore_rect = hscore_surface.get_rect(center=(hscore_x, hscore_y))
        screen.blit(hscore_surface, hscore_rect)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 255, 255), block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class FRUIT:
    def __init__(self):
        self.randomize()

    def randomize(self):
        # Create x and y position. We -1 from the cell_number so that the rectangle
        # doesn't end up outside the screen.

        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        # Create a rectangle that will be position on the x and y positions defined earlier.
        # We multiply the positions by cell_size so that the rectangle is placed on the grid.

        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)

        # Draw the rectangle

        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)


pygame.init()

# To create a grid, we set the size of each cell and the number of cells on each axis.

cell_size = 40
cell_number = 20

# The height and width of the screen is cell_size * cell_number

screen = pygame.display.set_mode((cell_size * cell_number, cell_size * (cell_number+2)))

clock = pygame.time.Clock()
game_font = pygame.font.Font('RetroGaming.ttf', 25)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

        if event.type == pygame.JOYBUTTONDOWN:
            if pygame.joystick.Joystick(0).get_button(3):
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if pygame.joystick.Joystick(0).get_button(0):
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if pygame.joystick.Joystick(0).get_button(2):
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if pygame.joystick.Joystick(0).get_button(1):
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

    screen.fill((0, 0, 0))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
