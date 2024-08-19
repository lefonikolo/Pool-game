import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Pygame window settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Το Μπιλιάρδο του Λευτέρη")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 128, 0)
brown = (139, 69, 19)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)
orange = (255, 165, 0)
maroon = (128, 0, 0)
dark_green = (0, 100, 0)

# Font
font = pygame.font.SysFont("comicsansms", 20)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Function to draw the table (board)
def draw_table():
    table_width, table_height = 800, 400
    table_top_left = ((screen_width - table_width) // 2, (screen_height - table_height) // 2)
    table_rect = pygame.Rect(table_top_left, (table_width, table_height))
    pygame.draw.rect(screen, brown, table_rect)

    cloth_margin = 20
    cloth_rect = pygame.Rect(table_top_left[0] + cloth_margin, table_top_left[1] + cloth_margin,
                             table_width - 2 * cloth_margin, table_height - 2 * cloth_margin)
    pygame.draw.rect(screen, green, cloth_rect)

    hole_radius = 25
    hole_positions = [
        (table_top_left[0] + hole_radius, table_top_left[1] + hole_radius),
        (table_top_left[0] + table_width - hole_radius, table_top_left[1] + hole_radius),
        (table_top_left[0] + hole_radius, table_top_left[1] + table_height - hole_radius),
        (table_top_left[0] + table_width - hole_radius, table_top_left[1] + table_height - hole_radius),
        (table_top_left[0] + table_width // 2, table_top_left[1] + hole_radius),
        (table_top_left[0] + table_width // 2, table_top_left[1] + table_height - hole_radius)
    ]

    for pos in hole_positions:
        pygame.draw.circle(screen, black, pos, hole_radius)

def draw_ball(color, pos, number=""):
    pygame.draw.circle(screen, color, pos, 15)
    if number:
        text_surface = font.render(str(number), True, black)
        screen.blit(text_surface, (pos[0] - text_surface.get_width() // 2, pos[1] - text_surface.get_height() // 2))

class Ball:
    def __init__(self, x, y, color, number=""):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.color = color
        self.number = number
        self.in_hole = False

    def draw(self):
        if not self.in_hole:
            draw_ball(self.color, (int(self.x), int(self.y)), self.number)

    def update(self):
        if not self.in_hole:
            self.x += self.vx
            self.y += self.vy
            self.vx *= 0.98
            self.vy *= 0.98
            if abs(self.vx) < 0.01:
                self.vx = 0
            if abs(self.vy) < 0.01:
                self.vy = 0
            self.check_bounds()

    def check_bounds(self):
        table_width, table_height = 800, 400
        table_top_left = ((screen_width - table_width) // 2, (screen_height - table_height) // 2)
        cloth_margin = 20

        min_x = table_top_left[0] + cloth_margin + 15
        max_x = table_top_left[0] + table_width - cloth_margin - 15
        min_y = table_top_left[1] + cloth_margin + 15
        max_y = table_top_left[1] + table_height - cloth_margin - 15

        if self.x < min_x:
            self.x = min_x
            self.vx = -self.vx
        if self.x > max_x:
            self.x = max_x
            self.vx = -self.vx
        if self.y < min_y:
            self.y = min_y
            self.vy = -self.vy
        if self.y > max_y:
            self.y = max_y
            self.vy = -self.vy

        # Check if the ball is in any hole
        hole_radius = 25
        hole_positions = [
            (table_top_left[0] + hole_radius, table_top_left[1] + hole_radius),
            (table_top_left[0] + table_width - hole_radius, table_top_left[1] + hole_radius),
            (table_top_left[0] + hole_radius, table_top_left[1] + table_height - hole_radius),
            (table_top_left[0] + table_width - hole_radius, table_top_left[1] + table_height - hole_radius),
            (table_top_left[0] + table_width // 2, table_top_left[1] + hole_radius),
            (table_top_left[0] + table_width // 2, table_top_left[1] + table_height - hole_radius)
        ]

        for pos in hole_positions:
            dx = self.x - pos[0]
            dy = self.y - pos[1]
            distance = math.hypot(dx, dy)
            if distance < hole_radius:
                print(f"Ball {self.number} entered hole at position {pos}")
                self.in_hole = True
                break

    def is_moving(self):
        return self.vx != 0 or self.vy != 0

def handle_collision(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.hypot(dx, dy)

    if distance < 30:
        normal_x = dx / distance
        normal_y = dy / distance

        tangent_x = -normal_y
        tangent_y = normal_x

        relative_velocity_x = ball2.vx - ball1.vx
        relative_velocity_y = ball2.vy - ball1.vy

        velocity_along_normal = (relative_velocity_x * normal_x +
                                 relative_velocity_y * normal_y)

        if velocity_along_normal < 0:
            j = -(1 + 1.0) * velocity_along_normal
            j /= 1 / 1.0 + 1 / 1.0

            impulse_x = j * normal_x
            impulse_y = j * normal_y
            ball1.vx -= impulse_x / 1
            ball1.vy -= impulse_y / 1
            ball2.vx += impulse_x / 1
            ball2.vy += impulse_y / 1

def new_game():
    balls = [
        Ball(screen_width // 4, screen_height // 2, white),
        Ball(screen_width // 2 + 30, screen_height // 2, red, "1"),
        Ball(screen_width // 2 + 60, screen_height // 2 - 15, yellow, "2"),
        Ball(screen_width // 2 + 60, screen_height // 2 + 15, blue, "3"),
        Ball(screen_width // 2 + 90, screen_height // 2 - 30, purple, "4"),
        Ball(screen_width // 2 + 90, screen_height // 2, black, "5"),
        Ball(screen_width // 2 + 90, screen_height // 2 + 30, maroon, "6"),
        Ball(screen_width // 2 + 120, screen_height // 2 - 45, dark_green, "7"),
        Ball(screen_width // 2 + 120, screen_height // 2 - 15, red, "8"),
        Ball(screen_width // 2 + 120, screen_height // 2 + 15, yellow, "9"),
        Ball(screen_width // 2 + 120, screen_height // 2 + 45, blue, "10"),
        Ball(screen_width // 2 + 150, screen_height // 2 - 60, purple, "11"),
        Ball(screen_width // 2 + 150, screen_height // 2 - 30, orange, "12"),
        Ball(screen_width // 2 + 150, screen_height // 2, maroon, "13"),
        Ball(screen_width // 2 + 150, screen_height // 2 + 30, dark_green, "14"),
        Ball(screen_width // 2 + 150, screen_height // 2 + 60, red, "15")
    ]

    cue_ball = balls[0]
    black_ball = balls[5]
    current_player = 0
    cue_ball_placed = True

    running = True
    shot_power = 0
    mouse_start_x, mouse_start_y = 0, 0
    game_over = False
    message = ""

    def check_other_balls():
        for ball in balls:
            if ball != black_ball and not ball.in_hole:
                return False
        return True

    while running:
        screen.fill((0, 128, 0))

        draw_table()

        for ball in balls:
            ball.update()
            ball.draw()

        if black_ball.in_hole and not game_over:
            if check_other_balls():
                message = "Νίκησες!"
            else:
                message = "Έχασες!"
            game_over = True

        if message:
            draw_text(message, font, red, screen, screen_width // 2, screen_height // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not cue_ball.is_moving() and cue_ball_placed:
                        mouse_start_x, mouse_start_y = event.pos

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if not cue_ball.is_moving() and cue_ball_placed and mouse_start_x != 0 and mouse_start_y != 0:
                        mouse_x, mouse_y = event.pos
                        dx = mouse_x - cue_ball.x
                        dy = mouse_y - cue_ball.y
                        distance = math.hypot(dx, dy)
                        if distance > 0:
                            cue_ball.vx = dx / distance * shot_power
                            cue_ball.vy = dy / distance * shot_power
                        shot_power = 0
                        current_player = 1 - current_player

                    mouse_start_x, mouse_start_y = 0, 0

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if cue_ball.in_hole:
                        cue_ball.x, cue_ball.y = event.pos
                        cue_ball.in_hole = False
                        cue_ball_placed = True

        if pygame.mouse.get_pressed()[0] and not cue_ball.is_moving() and cue_ball_placed:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - mouse_start_x
            dy = mouse_y - mouse_start_y
            shot_power = min(math.hypot(dx, dy) / 5, 20)

            cue_stick_end_x = cue_ball.x - dx
            cue_stick_end_y = cue_ball.y - dy

            pygame.draw.line(screen, brown, (cue_ball.x, cue_ball.y), (cue_stick_end_x, cue_stick_end_y), 5)

        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                handle_collision(balls[i], balls[j])

        pygame.display.flip()
        pygame.time.Clock().tick(60)

new_game()