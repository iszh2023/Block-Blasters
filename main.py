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
POWERUP_TYPES = ["widepaddle", "multiball", "fastball", "slowball", "bigball", "smallball", "stickypaddle", "laser", "shield", "bonus", "timefreeze", "magnetpaddle"]

# --- Colors ---
COLORS = {
    "background": (15, 15, 35),
    "background_gradient": [(15, 15, 35), (25, 25, 55)],
    "paddle": (60, 120, 255),
    "paddle_glow": (120, 180, 255),
    "ball": (255, 80, 120),
    "ball_trail": (255, 120, 160),
    "block": [(255, 80, 120), (80, 200, 255), (255, 200, 50), (160, 60, 210), (40, 220, 180), (250, 150, 40), (120, 240, 80), (255, 120, 200)],
    "block_power": [(255, 80, 120), (80, 200, 255), (255, 200, 50), (160, 60, 210), (40, 220, 180), (250, 150, 40), (120, 240, 80), (255, 120, 200)],
    "text": (255, 255, 255),
    "text_glow": (200, 200, 255),
    "widepaddle": (160, 60, 210),
    "multiball": (240, 20, 180),
    "fastball": (250, 150, 40),
    "slowball": (40, 220, 220),
    "bigball": (255, 100, 255),
    "smallball": (100, 255, 100),
    "stickypaddle": (180, 140, 60),
    "laser": (255, 50, 50),
    "shield": (100, 150, 255),
    "bonus": (255, 215, 0),
    "timefreeze": (200, 255, 255),
    "magnetpaddle": (255, 165, 0),
    "particle": (255, 255, 255),
    "explosion": [(255, 100, 100), (255, 150, 50), (255, 200, 0)]
}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Block Blasters')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 18)

# --- Game classes ---
class Ball:
    def __init__(self, x, y, vx, vy, speed=1.5):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.speed = float(speed)
        self.trail = []
        self.glow_radius = BALL_RADIUS + 3

    def move(self):
        # Add current position to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:
            self.trail.pop(0)
        
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

class Block:
    def __init__(self, x, y, powerup=None):
        self.x = x
        self.y = y
        self.alive = True
        self.powerup = powerup
        self.health = 1
        self.color_variant = random.randint(0, 7)
        self.glow_intensity = 0
        self.hit_animation = 0

class Powerup:
    def __init__(self, x, y, type_):
        self.x = x
        self.y = y
        self.vy = 0.4
        self.type = type_
        self.active = True
        self.rotation = 0
        self.pulse = 0
        self.particles = []

# --- Helper functions ---
def random_powerup():
    if random.random() < 0.25:  # Increased chance for more powerups
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

def draw_text(text, x, y, color=COLORS["text"], size=18, glow=False):
    tfont = pygame.font.SysFont('Arial', size, bold=True)
    
    if glow:
        # Create glow effect
        glow_surface = tfont.render(text, True, COLORS["text_glow"])
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx != 0 or dy != 0:
                    screen.blit(glow_surface, (x + dx, y + dy))
    
    surface = tfont.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_gradient_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(COLORS["background_gradient"][0][0] * (1 - ratio) + COLORS["background_gradient"][1][0] * ratio)
        g = int(COLORS["background_gradient"][0][1] * (1 - ratio) + COLORS["background_gradient"][1][1] * ratio)
        b = int(COLORS["background_gradient"][0][2] * (1 - ratio) + COLORS["background_gradient"][1][2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_glowing_ball(ball):
    # Draw trail
    for i, (tx, ty) in enumerate(ball.trail):
        alpha = (i + 1) / len(ball.trail)
        radius = int(BALL_RADIUS * alpha * 0.7)
        color = [int(c * alpha) for c in COLORS["ball_trail"]]
        if radius > 0:
            pygame.draw.circle(screen, color, (int(tx), int(ty)), radius)
    
    # Draw glow
    glow_surf = pygame.Surface((ball.glow_radius * 4, ball.glow_radius * 4), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (*COLORS["ball"], 30), (ball.glow_radius * 2, ball.glow_radius * 2), ball.glow_radius * 2)
    screen.blit(glow_surf, (int(ball.x) - ball.glow_radius * 2, int(ball.y) - ball.glow_radius * 2))
    
    # Draw main ball
    pygame.draw.circle(screen, COLORS["ball"], (int(ball.x), int(ball.y)), BALL_RADIUS)
    
    # Draw highlight
    pygame.draw.circle(screen, (255, 255, 255), (int(ball.x - 2), int(ball.y - 2)), BALL_RADIUS // 3)

def draw_detailed_block(block):
    if not block.alive:
        return
    
    # All blocks use the same colorful palette regardless of powerup status
    base_color = COLORS["block"][block.color_variant]
    
    # Add hit animation
    if block.hit_animation > 0:
        block.hit_animation -= 1
        shake_x = random.randint(-2, 2)
        shake_y = random.randint(-2, 2)
    else:
        shake_x = shake_y = 0
    
    # Draw shadow
    pygame.draw.rect(screen, (0, 0, 0), (block.x + shake_x + 2, block.y + shake_y + 2, BLOCK_W, BLOCK_H))
    
    # Draw main block
    pygame.draw.rect(screen, base_color, (block.x + shake_x, block.y + shake_y, BLOCK_W, BLOCK_H))
    
    # Draw border
    pygame.draw.rect(screen, (255, 255, 255), (block.x + shake_x, block.y + shake_y, BLOCK_W, BLOCK_H), 2)
    
    # Draw highlight
    pygame.draw.rect(screen, (255, 255, 255), (block.x + shake_x + 2, block.y + shake_y + 2, BLOCK_W - 4, 3))
    
    # Subtle glow effect for all blocks to maintain mystery
    block.glow_intensity = (block.glow_intensity + 0.1) % (2 * 3.14159)
    glow_alpha = int(15 + 10 * abs(pygame.math.Vector2(0, 1).rotate(block.glow_intensity * 180 / 3.14159).y))
    glow_surf = pygame.Surface((BLOCK_W + 6, BLOCK_H + 6), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (*base_color, glow_alpha), (0, 0, BLOCK_W + 6, BLOCK_H + 6))
    screen.blit(glow_surf, (block.x + shake_x - 3, block.y + shake_y - 3))

def draw_detailed_paddle(paddle_x, paddle_w, shield_active=False, magnet_active=False):
    # Draw shadow
    pygame.draw.rect(screen, (0, 0, 0), (paddle_x + 2, HEIGHT - 22, paddle_w, PADDLE_H))
    
    # Choose paddle color based on active effects
    paddle_color = COLORS["paddle"]
    if shield_active:
        paddle_color = COLORS["shield"]
    elif magnet_active:
        paddle_color = COLORS["magnetpaddle"]
    
    # Draw main paddle
    pygame.draw.rect(screen, paddle_color, (paddle_x, HEIGHT - 24, paddle_w, PADDLE_H))
    
    # Draw special effect glows
    if shield_active:
        # Shield glow
        shield_surf = pygame.Surface((paddle_w + 30, PADDLE_H + 30), pygame.SRCALPHA)
        pygame.draw.rect(shield_surf, (*COLORS["shield"], 80), (0, 0, paddle_w + 30, PADDLE_H + 30))
        screen.blit(shield_surf, (paddle_x - 15, HEIGHT - 39))
    elif magnet_active:
        # Magnetic field effect
        magnet_surf = pygame.Surface((paddle_w + 40, PADDLE_H + 40), pygame.SRCALPHA)
        pygame.draw.ellipse(magnet_surf, (*COLORS["magnetpaddle"], 60), (0, 0, paddle_w + 40, PADDLE_H + 40))
        screen.blit(magnet_surf, (paddle_x - 20, HEIGHT - 44))
    else:
        # Normal glow
        glow_surf = pygame.Surface((paddle_w + 20, PADDLE_H + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*COLORS["paddle_glow"], 50), (0, 0, paddle_w + 20, PADDLE_H + 20))
        screen.blit(glow_surf, (paddle_x - 10, HEIGHT - 34))
    
    # Draw highlight
    pygame.draw.rect(screen, (255, 255, 255), (paddle_x + 2, HEIGHT - 22, paddle_w - 4, 2))
    
    # Draw border
    pygame.draw.rect(screen, (255, 255, 255), (paddle_x, HEIGHT - 24, paddle_w, PADDLE_H), 2)

def draw_detailed_powerup(powerup):
    if not powerup.active:
        return
    
    powerup.rotation += 2
    powerup.pulse = (powerup.pulse + 0.3) % (2 * 3.14159)
    
    # Create pulsing effect
    pulse_size = int(POWERUP_SIZE + 3 * abs(pygame.math.Vector2(0, 1).rotate(powerup.pulse * 180 / 3.14159).y))
    
    # Draw glow
    glow_surf = pygame.Surface((pulse_size * 3, pulse_size * 3), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (*COLORS[powerup.type], 80), (pulse_size * 1.5, pulse_size * 1.5), pulse_size)
    screen.blit(glow_surf, (int(powerup.x) - pulse_size * 1.5, int(powerup.y) - pulse_size * 1.5))
    
    # Draw main powerup
    pygame.draw.circle(screen, COLORS[powerup.type], (int(powerup.x), int(powerup.y)), POWERUP_SIZE // 2)
    
    # Draw rotating border
    points = []
    for i in range(8):
        angle = (powerup.rotation + i * 45) * 3.14159 / 180
        x = int(powerup.x + (POWERUP_SIZE // 2 + 2) * pygame.math.Vector2(1, 0).rotate(angle * 180 / 3.14159).x)
        y = int(powerup.y + (POWERUP_SIZE // 2 + 2) * pygame.math.Vector2(1, 0).rotate(angle * 180 / 3.14159).y)
        points.append((x, y))
    
    if len(points) > 2:
        pygame.draw.polygon(screen, (255, 255, 255), points, 1)

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
    sticky_timer = 0
    shield_active = False
    shield_timer = 0
    time_frozen = False
    freeze_timer = 0
    magnet_active = False
    magnet_timer = 0

    def reset():
        nonlocal paddle_x, paddle_w, balls, blocks, powerups, score, game_over, powerup_timers, sticky_timer, shield_active, shield_timer, time_frozen, freeze_timer, magnet_active, magnet_timer
        paddle_x = WIDTH // 2 - PADDLE_W // 2
        paddle_w = PADDLE_W
        balls = [Ball(WIDTH // 2, HEIGHT - 40, 2, -3)]
        blocks = create_blocks()
        powerups = []
        score = 0
        game_over = False
        powerup_timers = {}
        sticky_timer = 0
        shield_active = False
        shield_timer = 0
        time_frozen = False
        freeze_timer = 0
        magnet_active = False
        magnet_timer = 0

    while running:
        # Draw detailed background
        draw_gradient_background()

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

        # Draw detailed blocks
        for block in blocks:
            draw_detailed_block(block)

        # Draw detailed paddle with special effects
        draw_detailed_paddle(paddle_x, paddle_w, shield_active, magnet_active)

        # Draw detailed balls
        for ball in balls:
            draw_glowing_ball(ball)

        # Draw detailed powerups
        for p in powerups:
            draw_detailed_powerup(p)

        # Draw score and status with glow
        draw_text(f"Score: {score}", 16, HEIGHT - 24, COLORS["text"], 20, glow=True)
        
        # Draw active powerup indicators
        status_y = 16
        if shield_active:
            draw_text("SHIELD", WIDTH - 100, status_y, COLORS["shield"], 16, glow=True)
            status_y += 25
        if magnet_active:
            draw_text("MAGNET", WIDTH - 100, status_y, COLORS["magnetpaddle"], 16, glow=True)
            status_y += 25
        if time_frozen:
            draw_text("FROZEN", WIDTH - 100, status_y, COLORS["timefreeze"], 16, glow=True)
            status_y += 25
        if sticky_timer > 0:
            draw_text("STICKY", WIDTH - 100, status_y, COLORS["stickypaddle"], 16, glow=True)

        # Ball movement and collisions only if not game over
        if not game_over and not time_frozen:
            # Move balls
            for ball in balls[:]:
                ball.move()
                
                # Magnet effect - attract balls to paddle
                if magnet_active:
                    paddle_center_x = paddle_x + paddle_w // 2
                    distance_x = paddle_center_x - ball.x
                    distance_y = (HEIGHT - 24) - ball.y
                    distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
                    
                    if distance < 100 and distance > 0:  # Magnet range
                        attract_force = 0.3
                        ball.vx += (distance_x / distance) * attract_force
                        ball.vy += (distance_y / distance) * attract_force
                # Wall bounce
                if ball.x <= BALL_RADIUS or ball.x >= WIDTH - BALL_RADIUS:
                    ball.vx *= -1
                if ball.y <= BALL_RADIUS:
                    ball.vy *= -1

                # Paddle bounce
                if (HEIGHT - 24 <= ball.y + BALL_RADIUS <= HEIGHT - 24 + PADDLE_H and
                    paddle_x < ball.x < paddle_x + paddle_w):
                    if sticky_timer > 0:
                        # Sticky paddle - ball sticks for a moment
                        ball.vy = 0
                        ball.vx = 0
                        sticky_timer -= 1
                    else:
                        ball.vy *= -1
                        hit_pos = (ball.x - paddle_x) / paddle_w
                        ball.vx = 2.0 * (hit_pos - 0.5)

                # Out of bounds (unless shield is active)
                if ball.y > HEIGHT + BALL_RADIUS:
                    if shield_active:
                        # Shield bounces ball back up
                        ball.y = HEIGHT - BALL_RADIUS
                        ball.vy *= -1
                        shield_timer -= 30  # Shield weakens with each save
                    else:
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
                            block.hit_animation = 10  # Add hit animation
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
                        elif p.type == "bigball":
                            for ball in balls:
                                ball.glow_radius = BALL_RADIUS + 8
                            powerup_timers["bigball"] = pygame.time.get_ticks()
                        elif p.type == "smallball":
                            for ball in balls:
                                ball.glow_radius = max(BALL_RADIUS - 3, 2)
                            powerup_timers["smallball"] = pygame.time.get_ticks()
                        elif p.type == "stickypaddle":
                            sticky_timer = 180  # 3 seconds at 60fps
                        elif p.type == "shield":
                            shield_active = True
                            shield_timer = 600  # 10 seconds
                        elif p.type == "bonus":
                            score += 100  # Bonus points
                        elif p.type == "timefreeze":
                            time_frozen = True
                            freeze_timer = 300  # 5 seconds
                        elif p.type == "magnetpaddle":
                            magnet_active = True
                            magnet_timer = 600  # 10 seconds
                    # Out of bounds
                    elif p.y > HEIGHT + POWERUP_SIZE:
                        p.active = False

            # Powerup duration and special timers
            now = pygame.time.get_ticks()
            
            # Timed powerups
            if "widepaddle" in powerup_timers and now - powerup_timers["widepaddle"] > 10000:
                paddle_w = PADDLE_W
                del powerup_timers["widepaddle"]
            if "fastball" in powerup_timers and now - powerup_timers["fastball"] > 10000:
                for ball in balls:
                    ball.speed = 1.5
                del powerup_timers["fastball"]
            if "slowball" in powerup_timers and now - powerup_timers["slowball"] > 10000:
                for ball in balls:
                    ball.speed = 1.5
                del powerup_timers["slowball"]
            if "bigball" in powerup_timers and now - powerup_timers["bigball"] > 8000:
                for ball in balls:
                    ball.glow_radius = BALL_RADIUS + 3
                del powerup_timers["bigball"]
            if "smallball" in powerup_timers and now - powerup_timers["smallball"] > 8000:
                for ball in balls:
                    ball.glow_radius = BALL_RADIUS + 3
                del powerup_timers["smallball"]
            
            # Frame-based timers
            if shield_timer > 0:
                shield_timer -= 1
            else:
                shield_active = False
                
            if freeze_timer > 0:
                freeze_timer -= 1
            else:
                time_frozen = False
                
            if magnet_timer > 0:
                magnet_timer -= 1
            else:
                magnet_active = False

        # Draw detailed game over screen
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            screen.blit(overlay, (0,0))
            
            # Check if all blocks destroyed (win condition)
            blocks_remaining = sum(1 for block in blocks if block.alive)
            if blocks_remaining == 0:
                draw_text("VICTORY!", WIDTH//2-60, HEIGHT//2-40, (100, 255, 100), 36, glow=True)
                draw_text(f"Final Score: {score}", WIDTH//2-80, HEIGHT//2-5, (255, 255, 255), 24, glow=True)
            else:
                draw_text("GAME OVER!", WIDTH//2-80, HEIGHT//2-40, (255, 100, 100), 36, glow=True)
                draw_text(f"Score: {score}", WIDTH//2-50, HEIGHT//2-5, (255, 255, 255), 24, glow=True)
            
            draw_text("Press SPACE to restart", WIDTH//2-110, HEIGHT//2+25, (200, 200, 255), 22, glow=True)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()