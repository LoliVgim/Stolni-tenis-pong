import pygame
import sys

# Inicijalizacija Pygame-a
pygame.init()

# Postavke prozora
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

# Postavke igre
clock = pygame.time.Clock()
fps = 60

# Postavke igrača
player_width, player_height = 15, 100
player_speed = 5
player1 = pygame.Rect(50, height // 2 - player_height // 2, player_width, player_height)
player2 = pygame.Rect(width - 50 - player_width, height // 2 - player_height // 2, player_width, player_height)

# Varijable za serviranje
serve_player1 = True
serve_player2 = False

# Glavna petlja igre
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    # Serviranje igrača 1
    if keys[pygame.K_SPACE] and serve_player1:
        serve_player1 = False
        serve_player2 = True

    # Serviranje igrača 2
    if keys[pygame.K_RETURN] and serve_player2:
        serve_player1 = True
        serve_player2 = False

    # Kontrole igrača 1
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= player_speed
    if keys[pygame.K_s] and player1.bottom < height:
        player1.y += player_speed

    if keys[pygame.K_a] and player1.left > 0:
        player1.x -= player_speed
    if keys[pygame.K_d] and player1.right < width // 2:
        player1.x += player_speed

    # Kontrole igrača 2
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= player_speed
    if keys[pygame.K_DOWN] and player2.bottom < height:
        player2.y += player_speed

    if keys[pygame.K_LEFT] and player2.left > width // 2:
        player2.x -= player_speed
    if keys[pygame.K_RIGHT] and player2.right < width:
        player2.x += player_speed

    # Ograničavanje igrača unutar svog polja
    player1.y = max(0, min(player1.y, height - player_height))
    player2.y = max(0, min(player2.y, height - player_height))
    player1.x = max(0, min(player1.x, width // 2 - player_width))
    player2.x = max(width // 2, min(player2.x, width - player_width))

    # Crtanje na ekran
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), player1)
    pygame.draw.rect(screen, (255, 255, 255), player2)

    # Ažuriranje prozora
    pygame.display.flip()

    # Postavljanje FPS-a
    clock.tick(fps)
