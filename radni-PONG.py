import pygame
import os

# Inicijalizacija Pygame-a
pygame.init()

# Postavke prozora
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong 3D")

# Postavke igre
ball_size = 20
ball_speed = [5, 5]
player_speed = 7
opponent_speed = 5

# Učitavanje slika
current_dir = os.path.dirname(__file__)
ball_image = pygame.image.load(os.path.join(current_dir, "ball.png")).convert_alpha()
player_image = pygame.image.load(os.path.join(current_dir, "player.png")).convert_alpha()
opponent_image = pygame.image.load(os.path.join(current_dir, "opponent.png")).convert_alpha()

# Promjena veličine slika
ball_image = pygame.transform.scale(ball_image, (ball_size, ball_size))
player_image = pygame.transform.scale(player_image, (100, 20))
opponent_image = pygame.transform.scale(opponent_image, (100, 20))

# Inicijalne pozicije
player_pos = [WIDTH // 2, HEIGHT - 20]
opponent_pos = [WIDTH // 2, 20]
ball_pos = [WIDTH // 2, HEIGHT // 2]

# Postavke stanja igre
is_game_active = False
score = {"player": 0, "opponent": 0}

# Funkcija za crtanje teksta na ekranu
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Glavna petlja igre
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Prikaz menija prije početka igre
    if not is_game_active:
        screen.fill((0, 0, 0))
        draw_text("Pong 3D", pygame.font.Font(None, 100), (255, 255, 255), WIDTH // 2, HEIGHT // 4)
        draw_text("Pritisnite SPACE za početak igre", pygame.font.Font(None, 36), (255, 255, 255), WIDTH // 2, HEIGHT // 2)

        if keys[pygame.K_SPACE]:
            is_game_active = True

    # Logika igre
    elif is_game_active:
        player_pos[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed

        # Logika lopte
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        # Odbijanje lopte od zidova
        if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH:
            ball_speed[0] = -ball_speed[0]

        # Odbijanje lopte od igrača i protivnika
        if (
            player_pos[1] <= ball_pos[1] <= player_pos[1] + 20
            and player_pos[0] <= ball_pos[0] <= player_pos[0] + 100
        ) or (
            opponent_pos[1] <= ball_pos[1] <= opponent_pos[1] + 20
            and opponent_pos[0] <= ball_pos[0] <= opponent_pos[0] + 100
        ):
            ball_speed[1] = -ball_speed[1]

        # Logika protivnika
        if opponent_pos[0] + 50 < ball_pos[0]:
            opponent_pos[0] += opponent_speed
        elif opponent_pos[0] + 50 > ball_pos[0]:
            opponent_pos[0] -= opponent_speed

        # Provjera pobjede
        if ball_pos[1] <= 0:
            score["player"] += 1
            is_game_active = False
            ball_pos = [WIDTH // 2, HEIGHT // 2]

        elif ball_pos[1] >= HEIGHT:
            score["opponent"] += 1
            is_game_active = False
            ball_pos = [WIDTH // 2, HEIGHT // 2]

        # Crtanje
        screen.fill((0, 0, 0))
        screen.blit(player_image, player_pos)
        screen.blit(opponent_image, opponent_pos)
        screen.blit(ball_image, ball_pos)

        draw_text(f"Igrač: {score['player']}  Protivnik: {score['opponent']}", pygame.font.Font(None, 36), (255, 255, 255), WIDTH // 2, 20)

    # Osvježavanje ekrana
    pygame.display.flip()

    # Postavljanje FPS-a
    clock.tick(FPS)

# Završavanje Pygame-a
pygame.quit()
