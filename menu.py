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
    
# Sound effect za gumbe
def play_click_sound():
    button_click_sound.play()

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
    global current_screen, game_started
    current_screen = "options"

# Igranje igrač protiv igrača
def start_1vs1_game():
    print("Započeta igra igrač protiv igrača!")

    
# Igranje protiv bota
def start_vs_bot_game():
    print("Započeta igra igrač protiv bota!")


def return_to_start():
    global current_screen
    current_screen = "start"

def options():
    print("Otvori opcije")

def achievements():
    print("Prikaži postignuća")

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
        draw_button("Opcije", screen_width // 2 - 100, 200 + 50 + 20, 200, 50, button_color, white, options)
        draw_button("Postignuća", screen_width // 2 - 100, 200 + 2 * (50 + 20), 200, 50, button_color, white, achievements)
        draw_button("Izađi", screen_width // 2 - 100, 200 + 3 * (50 + 20), 200, 50, button_color, white, exit_game)
    elif current_screen == "options":
        screen.blit(game_options_background, (0, 0))
        draw_button("1v1", screen_width // 4 - 100, 400, 200, 50, button_color, white, start_1vs1_game)
        draw_button("1 vs Bot", 3 * screen_width // 4 - 100, 400, 200, 50, button_color, white, start_vs_bot_game)
        draw_button("Povratak", screen_width // 2 - 100, 500, 200, 50, button_color, white, return_to_start)

    pygame.display.flip()
