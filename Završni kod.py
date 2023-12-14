import pygame
import sys
import os

pygame.init()

# Postavke prozora
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ICE Pong")

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
    pygame.display.set_caption("ICE Pong")

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
    text_color =(0,0,0)

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

            pygame.draw.rect(screen, (207, 159, 255), (menu_x, menu_y, menu_width, menu_height))

        # Prikaz menija
            menu_font = pygame.font.Font(None, 60)
            restart_text_surface = menu_font.render("Restart", True, text_color)
            menu_text_surface = menu_font.render("Izlaz", True, text_color)
        
        # Poruka koja pokazuje tko je pobijedio
            winner_font = pygame.font.Font(None, 45)
            winner_text_surface = winner_font.render(winner_text, True, text_color)
            winner_text_rect = winner_text_surface.get_rect(center=(menu_x + menu_width // 2, menu_y + 50))
            screen.blit(winner_text_surface, winner_text_rect.topleft)

        # veličina gumbova
            button_width = 400
            button_height = 75

            spacing = 20  

            restart_text_rect = pygame.Rect((menu_x + menu_width // 2 - button_width // 2, menu_y + menu_height // 2.2 - button_height - spacing, button_width, button_height))
            menu_text_rect = pygame.Rect((menu_x + menu_width // 2 - button_width // 2, menu_y + menu_height // 2.2 + spacing, button_width, button_height))

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
                        elif menu_text_rect.collidepoint(mouse_pos):
                             pygame.quit()
                             sys.exit()
                clock.tick(fps)
    
    
            

    # Crtanje na ekran
        screen.fill(background_color)
        pygame.draw.circle(screen, player1_color, player1.center, player_radius)
        pygame.draw.circle(screen, player2_color, player2.center, player_radius)
        pygame.draw.ellipse(screen, (255, 165, 0), ball)  # Naranèasta boja lopte

# Crtanje kruga u sredini ekrana
        center_circle_radius = height // 4  # Half of the vertical line
        center_circle_center = (width // 2, height // 2)
        pygame.draw.circle(screen, element_color, center_circle_center, center_circle_radius, 5)

# Crtanje paralelnih linija koje izlaze iz kruga
        line_length = center_circle_radius * 2  # Full length of the vertical line
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
        pygame.draw.ellipse(screen, (255, 165, 0), ball)  # Orange boja lopte

# Prikaz rezultata
        font = pygame.font.Font(None, 45)
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
    pygame.display.set_caption("ICE Pong")
    # Postavke igre
    clock = pygame.time.Clock()
    fps = 60

# Postavke igrača
    player_radius = 40
    player_speed = 6
    player1_color = (0, 255, 0)  # Zelena boja
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
    max_score = 5  # Maksimalan broj poena za pobjedu u igri
    text_color =(0,0,0)

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
            pygame.time.delay(500)  

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
            pygame.time.delay(500)  

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

            pygame.draw.rect(screen, (207, 159, 255), (menu_x, menu_y, menu_width, menu_height))

        # Prikaz menija
            menu_font = pygame.font.Font(None, 60)
            restart_text_surface = menu_font.render("Restart", True, text_color)
            menu_text_surface = menu_font.render("Izlaz", True, text_color)
        
        # Poruka koja pokazuje tko je pobijedio
            winner_font = pygame.font.Font(None, 45)
            winner_text_surface = winner_font.render(winner_text, True, text_color)
            winner_text_rect = winner_text_surface.get_rect(center=(menu_x + menu_width // 2, menu_y + 50))
            screen.blit(winner_text_surface, winner_text_rect.topleft)

        # veličina gumbova
            button_width = 400
            button_height = 75

            spacing = 20  

            restart_text_rect = pygame.Rect((menu_x + menu_width // 2 - button_width // 2, menu_y + menu_height // 2.2 - button_height - spacing, button_width, button_height))
            menu_text_rect = pygame.Rect((menu_x + menu_width // 2 - button_width // 2, menu_y + menu_height // 2.2 + spacing, button_width, button_height))

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
                        elif menu_text_rect.collidepoint(mouse_pos):
                             pygame.quit()
                             sys.exit()
                clock.tick(fps)
    
   


   # Crtanje na ekran
        screen.fill(background_color)
        pygame.draw.circle(screen, player1_color, player1.center, player_radius)
        pygame.draw.circle(screen, player2_color, player2.center, player_radius)
        pygame.draw.ellipse(screen, (255, 165, 0), ball)  # Narančasta boja lopte


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
        font = pygame.font.Font(None, 45)
        score_text = font.render(f"{score_player1} - {score_player2}", True, element_color)
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 10))

# Ažuriranje prozora
        pygame.display.flip()

    # Ažuriranje prozora
        pygame.display.flip()

    # Postavljanje FPS-a
        clock.tick(fps)

    


def return_to_start():
    global current_screen
    current_screen = "start"

#def options():
    #print("Otvori opcije")

#def achievements():
    #print("Prikaži postignuća")

def upute():
    global current_screen
    current_screen = "upute"
    
    # Upute
    upute_text = [
        "Upute:",
        " ",
        "1. Pritisnite 'Kreni' za početak igre.",
        " ",
        "2. Pritisnite '1v1' ili '1 vs Bot' kako biste započeli igru.",
        " ",
        "3. Kontrole za lijevog igrača: CRTL + WSAD",
        " ",
        "4. Kontrole za desnog igrača: Space + strelice"
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

    
    if current_screen == "start":
        screen.blit(background_image, (0, 0))
        draw_button("Kreni", screen_width // 2 - 100, 200 + (50 + 20), 200, 50, button_color, white, start_game)
        draw_button("Upute", screen_width // 2 - 100, 200 + 2* (50 + 20), 200, 50, button_color, white, upute)

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

