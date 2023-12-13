import pygame
import sys

# Inicijalizacija Pygame-a
pygame.init()

# Postavke prozora
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Stolni Tenis")

# Postavke igre
clock = pygame.time.Clock()
fps = 60

# Postavke igrača
player_radius = 40
player_speed = 7
player1_color = (0, 255, 0)  # Zelena boja
player2_color = (255, 0, 0)  # Crvena boja
player1 = pygame.Rect(50, height // 2 - player_radius, 2 * player_radius, 2 * player_radius)
player2 = pygame.Rect(width - 50 - player_radius * 2, height // 2 - player_radius, 2 * player_radius, 2 * player_radius)

# Postavke lopte
ball_size = 30  # Povećana veličina lopte
ball_speed = 7
ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)
ball_direction = (0, 0)  # Početni smjer

# Boje
background_color = (255, 255, 255)  # Bijela boja pozadine
element_color = (0, 0, 128)        # Tamnoplava boja mreže
score_color = (255, 255, 255)      # Bijela boja rezultata

# Serviranje
serve_player1 = True
serve_player2 = False

# Rezultati
score_player1 = 0
score_player2 = 0
servis_count = 0
max_servis_count = 2  # Broj servisa prije izmjene strane
max_score = 5  # Maksimalan broj poena za pobjedu u igri

# Dodatna postavka za provjeru servisa
is_serving = False
text_color = (0,0,0)
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

    elif ball.right >= width:
        score_player1 += 1
        servis_count = 0
        serve_player1 = False
        serve_player2 = True
        ball_direction = (0, 0)  # Zaustavi loptu
        ball.x = width // 2 - ball_size // 2
        ball.y = height // 2 - ball_size // 2
        is_serving = False

    # Izmjena strane nakon dva servisa
    if servis_count == max_servis_count:
        serve_player1, serve_player2 = serve_player2, serve_player1
        servis_count = 0

       # Provjera pobjednika
    if score_player1 == max_score or score_player2 == max_score:
        winner_text = "Zeleni igrač je pobijedio!" if score_player1 == max_score else "Crveni igrač je pobijedio!"

        # pozadina menija
        menu_width = width // 2
        menu_height = height // 2
        menu_x = (width - menu_width) // 2
        menu_y = (height - menu_height) // 2

        pygame.draw.rect(screen, (128, 0, 128), (menu_x, menu_y, menu_width, menu_height))

        # Prikaz menija
        menu_font = pygame.font.Font(None, 60)
        restart_text_surface = menu_font.render("Restart", True, text_color)
        menu_text_surface = menu_font.render("Return to Menu", True, text_color)
        
        # Poruka koja pokazuje tko je pobijedio
        winner_font = pygame.font.Font(None, 45)
        winner_text_surface = winner_font.render(winner_text, True, text_color)
        winner_text_rect = winner_text_surface.get_rect(center=(menu_x + menu_width // 2, menu_y + 50))
        screen.blit(winner_text_surface, winner_text_rect.topleft)

        # veličina gumbova
        button_width = 400
        button_height = 75

        spacing = 20  

        restart_text_rect = pygame.Rect((menu_x + menu_width // 2 - button_width // 2, menu_y + menu_height // 2 - button_height - spacing, button_width, button_height))
        menu_text_rect = pygame.Rect((menu_x + menu_width // 2 - button_width // 2, menu_y + menu_height // 2 + spacing, button_width, button_height))

        pygame.draw.rect(screen, element_color, restart_text_rect, 2)
        pygame.draw.rect(screen, element_color, menu_text_rect, 2)

        # Center-align 
        restart_text_rect.topleft = (menu_x + menu_width // 2 - restart_text_surface.get_width() // 2, menu_y + menu_height // 2 - button_height - spacing)
        screen.blit(restart_text_surface, restart_text_rect.topleft)

        menu_text_rect.topleft = (menu_x + menu_width // 2 - menu_text_surface.get_width() // 2, menu_y + menu_height // 2 + spacing)
        screen.blit(menu_text_surface, menu_text_rect.topleft)

        pygame.display.flip()

        # Čekanje igrača da klinu na meni
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Provjera je li igrač kliknuo restart ili return to menu
                    if restart_text_rect.collidepoint(mouse_pos):
                        # Resetiranje rezultata
                        score_player1 = 0
                        score_player2 = 0
                        servis_count = 0
                        serve_player1 = True
                        serve_player2 = False
                        is_serving = False
                        ball_direction = (0, 0)
                        ball.x = width // 2 - ball_size // 2
                        ball.y = height // 2 - ball_size // 2
                        waiting_for_input = False
                    elif menu_text_rect.collidepoint(mouse_pos): # Dio gdje Gui programeri moraju staviti svoj dio kako bi se korisnik ako želi vratio na glavni  menu
                        pygame.quit()
                        sys.exit()

            clock.tick(fps)


    # Crtanje na ekran
    screen.fill(background_color)
    pygame.draw.circle(screen, player1_color, player1.center, player_radius)
    pygame.draw.circle(screen, player2_color, player2.center, player_radius)
    pygame.draw.ellipse(screen, (255, 165, 0), ball)  

    # Crtanje kruga u sredini ekrana
    center_circle_radius = height // 4  
    center_circle_center = (width // 2, height // 2)
    pygame.draw.circle(screen, element_color, center_circle_center, center_circle_radius, 5)

    # Crtanje paralelnih linija koje izlaze iz kruga
    line_length = center_circle_radius * 2  
    line_start = (center_circle_center[0], center_circle_center[1] - center_circle_radius)
    line_end = (center_circle_center[0], center_circle_center[1] + center_circle_radius)
    pygame.draw.line(screen, element_color, line_start, line_end, 5)

    # Crtanje na ekran
    screen.fill(background_color)
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
    pygame.draw.ellipse(screen, (255, 165, 0), ball)  #     Narančatsa boja lopte

    # Prikaz rezultata
    font = pygame.font.Font(None, 45)
    score_text = font.render(f"{score_player1} - {score_player2}", True, element_color)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 10))

    # Ažuriranje prozora
    pygame.display.flip()


    # Postavljanje FPS-a
    clock.tick(fps)

