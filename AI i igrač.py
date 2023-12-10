import pygame
import sys
import random

# Inicijalizacija Pygame-a
pygame.init()

# Postavke prozora
width, height = 1280, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Stolni Tenis")

# Postavke igre
clock = pygame.time.Clock()
fps = 60

# Postavke igrača
player_radius = 40
player_speed = 6
player1_color = (0, 0, 255)  # Plava boja
player2_color = (255, 0, 0)  # Crvena boja
player1 = pygame.Rect(50, height // 2 - player_radius, 2 * player_radius, 2 * player_radius)
player2 = pygame.Rect(width - 50 - player_radius * 2, height // 2 - player_radius, 2 * player_radius, 2 * player_radius)

# Postavke AI igrača
ai_speed = 6

# Postavke lopte
ball_size = 30  # Povećana veličina lopte
ball_speed = 7
ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)
ball_direction = (0, 0)  # Početni smjer

# Boje
background_color = (255, 255, 255)  # Zelena boja pozadine
element_color = (0, 0, 128)  # Boja mreže
score_color = (255, 255, 255)  # Boja rezultata

# Serviranje
serve_player1 = True
serve_player2 = False

# Rezultati
score_player1 = 0
score_player2 = 0
servis_count = 0
max_servis_count = 2  # Broj servisa prije izmjene strane
max_score = 11  # Maksimalan broj poena za pobjedu u igri

# Dodatna postavka za provjeru servisa
is_serving = False

# Dodatna postavka za provjeru servisa
is_serving = False

# Glavna petlja igre
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    # Kontrole igrača 1
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= player_speed
    if keys[pygame.K_s] and player1.bottom < height:
        player1.y += player_speed
    if keys[pygame.K_a] and player1.left > 0:
        player1.x -= player_speed
    if keys[pygame.K_d] and player1.right < width // 2:
        player1.x += player_speed

   # AI kontrola igrača 2
    if player2.centery < ball.centery and player2.bottom < height:
        player2.y += ai_speed
    elif player2.centery > ball.centery and player2.top > 0:
        player2.y -= ai_speed

# Serviranje igrača 1
    if keys[pygame.K_LCTRL] and serve_player1 and not is_serving:
        serve_player1 = False
        serve_player2 = True
        ball_direction = (1, -1)  # Lopta uvijek ide prema gornjem lijevom kutu
        ball.x = player1.right + 1  # Postavljanje lopte desno od igrača 1
        ball.y = player1.centery - ball_size // 2
        servis_count += 1
        is_serving = True

# Serviranje igrača 2
    if keys[pygame.K_SPACE] and serve_player2 and not is_serving:
        serve_player1 = True
        serve_player2 = False
        ball_direction = (-1, 1)  # Lopta uvijek ide prema donjem desnom kutu
        ball.x = player2.left - ball_size - 1  # Postavljanje lopte lijevo od igrača 2
        ball.y = player2.centery - ball_size // 2
        servis_count += 1
        is_serving = True

# Pomicanje lopte samo nakon servisa
    if ball_direction != (0, 0):
        ball.x += ball_speed * ball_direction[0]
        ball.y += ball_speed * ball_direction[1]

    # Odbijanje lopte od vrha i dna
        if ball.top <= 0 or ball.bottom >= height:
            ball_direction = (ball_direction[0], -ball_direction[1])

    # Odbijanje lopte od lijevog i desnog ruba
        if ball.left <= 0 or ball.right >= width:
            ball_direction = (-ball_direction[0], ball_direction[1])

    # Odbijanje lopte od igrača 1
        if ball.colliderect(player1):
            ball_direction = (abs(ball_direction[0]), ball_direction[1])
            if player1.x < width // 2:
                ball.x = player1.right + 1
            else:
                ball.x = player1.left - ball_size - 1

    # Odbijanje lopte od igrača 2
        if ball.colliderect(player2):
            ball_direction = (-abs(ball_direction[0]), ball_direction[1])
            if player2.x < width // 2:
                ball.x = player2.right + 1
            else:
                ball.x = player2.left - ball_size - 1


    if ball.left <= 0 or ball.right >= width:
        is_serving = False

    # Pomicanje igrača unutar granica
    player1.y = max(0, min(player1.y, height - player1.height))
    player2.y = max(0, min(player2.y, height - player2.height))
    player1.x = max(0, min(player1.x, width // 2 - player1.width))
    player2.x = max(width // 2, min(player2.x, width - player2.width))

    # Ako lopta prođe lijevi ili desni zid, povećaj rezultat i resetiraj servis
    if ball.left <= 0:
        score_player2 += 1
        servis_count = 0
        serve_player1 = True
        serve_player2 = False
        ball_direction = (0, 0)  # Zaustavi loptu
        ball.x = width // 2 - ball_size // 2
        ball.y = height // 2 - ball_size // 2
        is_serving = False

        # Resetiraj poziciju AI igrača i zaustavi ga na kratko vrijeme
        player2.y = height // 2 - player_radius
        pygame.time.delay(500)  # Pause for 500 milliseconds (0.5 seconds)

    elif ball.right >= width:
        score_player1 += 1
        servis_count = 0
        serve_player1 = False
        serve_player2 = True
        ball_direction = (0, 0)  # Zaustavi loptu
        ball.x = width // 2 - ball_size // 2
        ball.y = height // 2 - ball_size // 2
        is_serving = False

        # Resetiraj poziciju AI igrača i zaustavi ga na kratko vrijeme
        player2.y = height // 2 - player_radius
        pygame.time.delay(500)  # Pause for 500 milliseconds (0.5 seconds)

    # Izmjena strane nakon dva servisa
    if servis_count == max_servis_count:
        serve_player1, serve_player2 = serve_player2, serve_player1
        servis_count = 0

    # Provjera pobjednika
    if score_player1 == max_score or score_player2 == max_score:
        print("Kraj igre!")
        pygame.quit()
        sys.exit()

   # Crtanje na ekran
    screen.fill(background_color)
    pygame.draw.circle(screen, player1_color, player1.center, player_radius)
    pygame.draw.circle(screen, player2_color, player2.center, player_radius)
    pygame.draw.ellipse(screen, (255, 165, 0), ball)  # Orange boja lopte


# Crtanje kruga u sredini ekrana
    center_circle_radius = height // 4  # Polovica vertikalne linije
    center_circle_center = (width // 2, height // 2)
    pygame.draw.circle(screen, element_color, center_circle_center, center_circle_radius, 5)

# Crtanje paralelnih linija koje izlaze iz kruga
    line_length = center_circle_radius * 2  # Puna duljina vertikalne linije
    line_start = (center_circle_center[0], center_circle_center[1] - center_circle_radius)
    line_end = (center_circle_center[0], center_circle_center[1] + center_circle_radius)
    pygame.draw.line(screen, element_color, line_start, line_end, 5)

# Crtanje na ekran
    screen.fill(background_color)

# Nacrtajte krug i linije prije nego što nacrtate igrače i loptu
    pygame.draw.circle(screen, element_color, center_circle_center, center_circle_radius, 5)
    pygame.draw.line(screen, element_color, line_start, line_end, 5)

# Crtanje mreže
    pygame.draw.line(screen, element_color, (width // 2, 0), (width // 2, height), 10)

# Crtanje podebljane bijele horizontalne crte u sredini ekrana
    pygame.draw.line(screen, element_color, (0, height // 2), (width, height // 2), 4)

# Crtanje podebljanih linija uz rub prozora
    pygame.draw.line(screen, element_color, (0, 0), (0, height), 10)
    pygame.draw.line(screen, element_color, (width - 1, 0), (width - 1, height), 10)

# Crtanje podebljanih linija na kraju stola
    pygame.draw.line(screen, element_color, (0, 0), (0, height), 10)
    pygame.draw.line(screen, element_color, (width - 1, 0), (width - 1, height), 10)
    
# Dodatne podebljane linije uz rub stola
    pygame.draw.line(screen, element_color, (0, 0), (width, 0), 10)
    pygame.draw.line(screen, element_color, (0, height - 1), (width, height - 1), 10)

# Crtanje kruga iznad linija
    pygame.draw.circle(screen, player1_color, player1.center, player_radius)
    pygame.draw.circle(screen, player2_color, player2.center, player_radius)

# Crtanje lopte
    pygame.draw.ellipse(screen, (255, 165, 0), ball)  # Narančasta boja lopte

# Prikaz rezultata
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"{score_player1} - {score_player2}", True, element_color)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 10))

# Ažuriranje prozora
    pygame.display.flip()

    # Ažuriranje prozora
    pygame.display.flip()

    # Postavljanje FPS-a
    clock.tick(fps)


