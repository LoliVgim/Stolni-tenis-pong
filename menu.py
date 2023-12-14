import pygame
import sys
import os

pygame.init()

# Postavke prozora
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Pozadina
background_image_path = os.path.join("pozadina.jpg")
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

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
    print("Igra je započela!")

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

    # Pozadina
    screen.blit(background_image, (0, 0))


    # Crtanje gumbova
    button_width, button_height = 200, 70
    button_spacing = 20
    draw_button("Kreni", screen_width // 2 - button_width // 2, 200, button_width, button_height, button_color, white, start_game)
    draw_button("Opcije", screen_width // 2 - button_width // 2, 200 + button_height + button_spacing, button_width, button_height, button_color, white, options)
    draw_button("Postignuća", screen_width // 2 - button_width // 2, 200 + 2 * (button_height + button_spacing), button_width, button_height, button_color, white, achievements)
    draw_button("Izađi", screen_width // 2 - button_width // 2, 200 + 3 * (button_height + button_spacing), button_width, button_height, button_color, white, exit_game)

    pygame.display.flip()
