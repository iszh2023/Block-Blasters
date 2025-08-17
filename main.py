import pygame
import random
import sys

# --- Constants ---
WIDTH, HEIGHT = 600, 400
PADDLE_W, PADDLE_H = 80, 12
BALL_RADIUS = 8
BLOCK_ROWS, BLOCK_COLS = 5, 8
BLOCK_W, BLOCK_H = 62, 18
POWERUP_SIZE = 14

# --- Powerup Types ---
POWERUP_TYPES = ["widepaddle", "multiball", "fastball", "slowball"]

# --- Colors ---
COLORS = {
    "background": (230, 235, 255),
    "paddle": (40, 80, 230),
    "ball": (220, 40, 60),
    "block": (40, 200, 60),
    "block_power": (230, 200, 30),
    "text": (30, 30, 30),
    "widepaddle": (160, 60, 210),
    "multiball": (240, 20, 180),
    "fastball": (250, 150, 40),
    "slowball": (40, 220, 220)
}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Block Blasters')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 18)

# --- Game classes ---
class Ball:
    def __init__(self, x, y, vx, vy, speed=4):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.speed = speed

    def move(self):
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

class Block:
    def __init__(self, x, y, powerup=None):
        self.x = x
        self.y = y
        self.alive = True
        self.powerup = powerup

class Powerup:
    def __init__(self, x, y, type_):
        self.x = x
        self.y = y
        self.vy = 2
        self.type = type_
        self.active = True

# --- Helper functions ---
def random_powerup():
    if random.random() < 0.15:
        return random.choice(POWERUP_TYPES)
    return None

def create_blocks():
    blocks = []
    for row in range(BLOCK_ROWS):
        for col in range(BLOCK_COLS):
            x = col * (BLOCK_W + 8) + 16
            y = row * (BLOCK_H + 8) + 32
            powerup = random_powerup()
            blocks.append(Block(x, y, powerup))
    return blocks

def draw_text(text, x, y, color=COLORS["text"], size=18):
    tfont = pygame.font.SysFont('Arial', size)
    surface = tfont.render(text, True, color)
    screen.blit(surface, (x, y))

# --- Main game function ---
def main():
    running = True
    paddle_x = WIDTH // 2 - PADDLE_W // 2
    paddle_w = PADDLE_W
    balls = [Ball(WIDTH // 2, HEIGHT - 40, 2, -3)]
    blocks = create_blocks()
    powerups = []
    score = 0
    game_over = False
    powerup_timers = {}

    def reset():
        nonlocal paddle_x, paddle_w, balls, blocks, powerups, score, game_over, powerup_timers
        paddle_x = WIDTH // 2 - PADDLE_W // 2
        paddle_w = PADDLE_W
        balls = [Ball(WIDTH // 2, HEIGHT - 40, 2, -3)]
        blocks = create_blocks()
        powerups = []
        score = 0
        game_over = False
        powerup_timers = {}

    while running:
        screen.fill(COLORS["background"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    reset()

        # Paddle controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle_x = max(0, paddle_x - 8)
        if keys[pygame.K_RIGHT]:
            paddle_x = min(WIDTH - paddle_w, paddle_x + 8)

        # Draw blocks
        for block in blocks:
            if block.alive:
                color = COLORS["block_power"] if block.powerup else COLORS["block"]
                pygame.draw.rect(screen, color, (block.x, block.y, BLOCK_W, BLOCK_H))

        # Draw paddle
        pygame.draw.rect(screen, COLORS["paddle"], (paddle_x, HEIGHT - 24, paddle_w, PADDLE_H))

        # Draw balls
        for ball in balls:
            pygame.draw.circle(screen, COLORS["ball"], (int(ball.x), int(ball.y)), BALL_RADIUS)

        # Draw powerups
        for p in powerups:
            if p.active:
                pygame.draw.circle(screen, COLORS[p.type], (int(p.x), int(p.y)), POWERUP_SIZE // 2)

        # Draw score
        draw_text(f"Score: {score}", 16, HEIGHT - 24)

        # Ball movement and collisions only if not game over
        if not game_over:
            # Move balls
            for ball in balls[:]:
                ball.move()
                # Wall bounce
                if ball.x <= BALL_RADIUS or ball.x >= WIDTH - BALL_RADIUS:
                    ball.vx *= -1
                if ball.y <= BALL_RADIUS:
                    ball.vy *= -1

                # Paddle bounce
                if (HEIGHT - 24 <= ball.y + BALL_RADIUS <= HEIGHT - 24 + PADDLE_H and
                    paddle_x < ball.x < paddle_x + paddle_w):
                    ball.vy *= -1
                    hit_pos = (ball.x - paddle_x) / paddle_w
                    ball.vx = 2 * (hit_pos - 0.5)

                # Out of bounds
                if ball.y > HEIGHT + BALL_RADIUS:
                    balls.remove(ball)

            if not balls:
                game_over = True

            # Block collisions
            for block in blocks:
                if block.alive:
                    for ball in balls:
                        if (block.x < ball.x < block.x + BLOCK_W and
                            block.y < ball.y < block.y + BLOCK_H):
                            block.alive = False
                            ball.vy *= -1
                            score += 10
                            if block.powerup:
                                powerups.append(Powerup(block.x + BLOCK_W//2, block.y + BLOCK_H//2, block.powerup))
                            break

            # Powerup falling
            for p in powerups:
                if p.active:
                    p.y += p.vy
                    # Paddle catch
                    if (HEIGHT - 24 <= p.y + POWERUP_SIZE//2 <= HEIGHT - 24 + PADDLE_H and
                        paddle_x < p.x < paddle_x + paddle_w):
                        # Activate powerup
                        p.active = False
                        if p.type == "widepaddle":
                            paddle_w = min(paddle_w * 1.6, WIDTH // 2)
                            powerup_timers["widepaddle"] = pygame.time.get_ticks()
                        elif p.type == "multiball":
                            balls.append(Ball(WIDTH//2, HEIGHT-40, 2, -2))
                            balls.append(Ball(WIDTH//2, HEIGHT-40, -2, -3))
                        elif p.type == "fastball":
                            for ball in balls:
                                ball.speed *= 1.5
                            powerup_timers["fastball"] = pygame.time.get_ticks()
                        elif p.type == "slowball":
                            for ball in balls:
                                ball.speed *= 0.7
                            powerup_timers["slowball"] = pygame.time.get_ticks()
                    # Out of bounds
                    elif p.y > HEIGHT + POWERUP_SIZE:
                        p.active = False

            # Powerup duration
            now = pygame.time.get_ticks()
            if "widepaddle" in powerup_timers and now - powerup_timers["widepaddle"] > 10000:
                paddle_w = PADDLE_W
                del powerup_timers["widepaddle"]
            if "fastball" in powerup_timers and now - powerup_timers["fastball"] > 10000:
                for ball in balls:
                    ball.speed = 4
                del powerup_timers["fastball"]
            if "slowball" in powerup_timers and now - powerup_timers["slowball"] > 10000:
                for ball in balls:
                    ball.speed = 4
                del powerup_timers["slowball"]

        # Draw game over text
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,140))
            screen.blit(overlay, (0,0))
            draw_text("GAME OVER!", WIDTH//2-80, HEIGHT//2-24, (255,255,255), 32)
            draw_text("Press SPACE to restart", WIDTH//2-110, HEIGHT//2+18, (255,255,255), 22)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()