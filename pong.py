import pygame
import sys
import os

pygame.init()

# Postavke prozora
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Pozadine
background_image_path = os.path.join("pozadina_start.jpg")
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

game_options_background_path = os.path.join("pozadina_options.jpg")
game_options_background = pygame.image.load(game_options_background_path)
game_options_background = pygame.transform.scale(game_options_background, (screen_width, screen_height))

game_instructions_background_path = os.path.join("pozadina_upute.jpg")
game_instructions_background = pygame.image.load(game_instructions_background_path)
game_instructions_background = pygame.transform.scale(game_instructions_background, (screen_width, screen_height))

# Za promjenu pozadine
current_screen = "start"

# Boje
black = (0, 0, 0)
white = (255, 255, 255)
button_color = (50, 50, 50)

# Font
font = pygame.font.SysFont("gillsansultracondensed", 36)

def draw_text(text, x, y, color=white):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    
# Crtanje gumba
def draw_button(text, x, y, width, height, button_color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, button_color, (x, y, width, height))

    draw_text(text, x + width // 2, y + height // 2)


# Akcije gumba
def start_game():
    global current_screen
    current_screen = "options"

# Igranje igrač protiv igrača
def start_1vs1_game():
        # Postavke prozora
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")

    # Postavke igre
    clock = pygame.time.Clock()
    fps = 60

    # Postavke igrača
    player_radius = 40
    player_speed = 7
    player1_color = (0, 0, 255)  # Plava boja
    player2_color = (255, 0, 0)  # Crvena boja
    player1 = pygame.Rect(50, height // 2 - player_radius, 2 * player_radius, 2 * player_radius)
    player2 = pygame.Rect(width - 50 - player_radius * 2, height // 2 - player_radius, 2 * player_radius, 2 * player_radius)

    # Postavke lopte
    ball_size = 30  # Povećana veličina lopte
    ball_speed = 7
    ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)
    ball_direction = (0, 0)  # Početni smjer

    # Boje
    background_color = (0, 128, 0)  # Zelena boja pozadine
    element_color = (255, 255, 255)  # Boja mreže
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

    # Glavna petlja igre
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        # Kontrole igrača 2
        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= player_speed
        if keys[pygame.K_DOWN] and player2.bottom < height:
            player2.y += player_speed
        if keys[pygame.K_LEFT] and player2.left > width // 2:
            player2.x -= player_speed
        if keys[pygame.K_RIGHT] and player2.right < width:
            player2.x += player_speed

        # Serviranje igrača 1
        if keys[pygame.K_LCTRL] and serve_player1:
            serve_player1 = False
            serve_player2 = True
            ball_direction = (1, -1)  # Lopta uvijek ide prema gornjem lijevom kutu
            ball.x = player1.right + 1  # Postavljanje lopte desno od igrača 1
            ball.y = player1.centery - ball_size // 2
            servis_count += 1

        # Serviranje igrača 2
        if keys[pygame.K_SPACE] and serve_player2:
            serve_player1 = True
            serve_player2 = False
            ball_direction = (-1, 1)  # Lopta uvijek ide prema donjem desnom kutu
            ball.x = player2.left - ball_size - 1  # Postavljanje lopte lijevo od igrača 2
            ball.y = player2.centery - ball_size // 2
            servis_count += 1

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

        elif ball.right >= width:
            score_player1 += 1
            servis_count = 0
            serve_player1 = False
            serve_player2 = True
            ball_direction = (0, 0)  # Zaustavi loptu
            ball.x = width // 2 - ball_size // 2
            ball.y = height // 2 - ball_size // 2

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
        pygame.draw.ellipse(screen, element_color, ball)

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

        # Crtanje paralelnih linija uz središnju horizontalnu crtu
        

        # Dodavanje horizontalnih linija uz rub stola
        pygame.draw.line(screen, element_color, (0, 0), (width, 0), 5)
        pygame.draw.line(screen, element_color, (0, height - 1), (width, height - 1), 5)
        # Prikaz rezultata
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"{score_player1} - {score_player2}", True, element_color)
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 10))

        # Ažuriranje prozora
        pygame.display.flip()

        # Postavljanje FPS-a
        clock.tick(fps)


    
# Igranje protiv bota
def start_vs_bot_game():
    # Postavke prozora
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")

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
    background_color = (0, 128, 0)  # Zelena boja pozadine
    element_color = (255, 255, 255)  # Boja mreže
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

    # Glavna petlja igre
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
        if keys[pygame.K_LCTRL] and serve_player1:
            serve_player1 = False
            serve_player2 = True
            ball_direction = (1, -1)  # Lopta uvijek ide prema gornjem lijevom kutu
            ball.x = player1.right + 1  # Postavljanje lopte desno od igrača 1
            ball.y = player1.centery - ball_size // 2
            servis_count += 1

        # Serviranje igrača 2
        if keys[pygame.K_SPACE] and serve_player2:
            serve_player1 = True
            serve_player2 = False
            ball_direction = (-1, 1)  # Lopta uvijek ide prema donjem desnom kutu
            ball.x = player2.left - ball_size - 1  # Postavljanje lopte lijevo od igrača 2
            ball.y = player2.centery - ball_size // 2
            servis_count += 1

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

        elif ball.right >= width:
            score_player1 += 1
            servis_count = 0
            serve_player1 = False
            serve_player2 = True
            ball_direction = (0, 0)  # Zaustavi loptu
            ball.x = width // 2 - ball_size // 2
            ball.y = height // 2 - ball_size // 2

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
        pygame.draw.ellipse(screen, element_color, ball)

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



        # Dodavanje horizontalnih linija uz rub stola
        pygame.draw.line(screen, element_color, (0, 0), (width, 0), 5)
        pygame.draw.line(screen, element_color, (0, height - 1), (width, height - 1), 5)

        # Prikaz rezultata
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"{score_player1} - {score_player2}", True, element_color)
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 10))

        # Ažuriranje prozora
        pygame.display.flip()

        # Postavljanje FPS-a
        clock.tick(fps)



def return_to_start():
    global current_screen
    current_screen = "start"

def options():
    print("Otvori opcije")

def achievements():
    print("Prikaži postignuća")

def upute():
    global current_screen
    current_screen = "upute"
    
    # Upute
    upute_text = [
        "Upute:",
        "1. Pritisnite 'Kreni' za početak igre.",
        "2. Pritisnite '1v1' ili '1 vs Bot' kako biste započeli igru."
    ]

    y_offset = screen_height // 4 + 20
    for line in upute_text:
        text_surface = font.render(line, True, black)
        text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += 30


def exit_game():
    pygame.quit()
    sys.exit()


# Glavna petlja
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(black)

    # Pozadine
    if current_screen == "start":
        screen.blit(background_image, (0, 0))
        draw_button("Kreni", screen_width // 2 - 100, 200, 200, 50, button_color, white, start_game)
        draw_button("Upute", screen_width // 2 - 100, 200 + 50 + 20, 200, 50, button_color, white, upute)
        draw_button("Opcije", screen_width // 2 - 100, 200 + 2 * (50 + 20), 200, 50, button_color, white, options)
        draw_button("Postignuća", screen_width // 2 - 100, 200 + 3 * (50 + 20), 200, 50, button_color, white, achievements)
        draw_button("Izađi", screen_width // 2 - 100, 200 + 5 * (50 + 20), 200, 50, button_color, white, exit_game)
    elif current_screen == "options":
        screen.blit(game_options_background, (0, 0))
        draw_button("1v1", screen_width // 4 - 100, 400, 200, 50, button_color, white, start_1vs1_game)
        draw_button("1 vs Bot", 3 * screen_width // 4 - 100, 400, 200, 50, button_color, white, start_vs_bot_game)
        draw_button("Povratak", screen_width // 2 - 100, 500, 200, 50, button_color, white, return_to_start)
    elif current_screen == "upute":
        screen.blit(game_instructions_background, (0, 0))
        upute()
        draw_button("Povratak", screen_width // 2 - 100, 500, 200, 50, button_color, white, return_to_start)
        

    pygame.display.flip()
