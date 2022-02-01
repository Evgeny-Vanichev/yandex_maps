import pygame
import sys
from io import BytesIO
from API_module import *


def load_image():
    # Получение картинки с координатами coords
    map_params['ll'] = f'{long},{lat}'
    map_params['spn'] = f'{spn},{spn}'
    map_response = load_map(map_params=map_params)
    return BytesIO(map_response.content)


def search_object():
    global response, long, lat, map_params, current_text, spn
    response = geocoder_request(current_text)
    try:
        long, lat, spn, spn = get_geo_data(response)
    except IndexError:
        current_text = "Неверный запрос"
        screen.blit(font.render(current_text, True, (190, 20, 20)), (10, 15))
        return
    map_params = get_map_params(response)


# Получение координат объекта target
response, long, lat, map_params = [None] * 4
current_text = "Москва"
insert_text = False
search_object()
spn = 0.3 / 4
pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
screen.blit(pygame.image.load(load_image()), (200, 50))
look_sat = pygame.draw.rect(screen, pygame.Color("black"), (100, 150, 50, 50), 0)
look_map = pygame.draw.rect(screen, pygame.Color("black"), (100, 250, 50, 50), 0)
look_skl = pygame.draw.rect(screen, pygame.Color("black"), (100, 350, 50, 50), 0)
font = pygame.font.Font(None, 30)
text1 = font.render("sat", True, (255, 255, 255))
screen.blit(text1, (110, 165))
text2 = font.render("map", True, (255, 255, 255))
screen.blit(text2, (105, 265))
text3 = font.render("skl", True, (255, 255, 255))
screen.blit(text3, (110, 365))
text_box = pygame.draw.rect(screen, (240, 240, 240), (10, 10, 780, 30))
text = font.render(current_text, True, (0, 0, 0))
screen.blit(text, (10, 15))
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            delta = spn
            if event.key == pygame.K_DOWN:
                lat -= delta
            elif event.key == pygame.K_UP:
                lat += delta
            elif event.key == pygame.K_RIGHT:
                long += delta * 1.85
            elif event.key == pygame.K_LEFT:
                long -= delta * 1.85
            if event.key == pygame.K_PAGEDOWN:
                spn *= 2
            if event.key == pygame.K_PAGEUP:
                if spn > 0.001:
                    spn /= 2
            else:
                if event.key == pygame.K_BACKSPACE:
                    current_text = current_text[:-1]
                elif event.key == pygame.K_RETURN:
                    search_object()
                    insert_text = False
                else:
                    current_text += event.unicode
                text_box = pygame.draw.rect(screen, (240, 240, 240), (10, 10, 780, 30))
                text = font.render(current_text, True, (0, 0, 0))
                screen.blit(text, (10, 15))
            screen.blit(pygame.image.load(load_image()), (200, 50))
            pygame.display.flip()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if text_box.collidepoint(event.pos):
                insert_text = True
            else:
                insert_text = False
            if look_sat.collidepoint(event.pos):
                map_params['l'] = "sat"
            elif look_map.collidepoint(event.pos):
                map_params['l'] = "map"
            elif look_skl.collidepoint(event.pos):
                map_params['l'] = "skl"
            screen.blit(pygame.image.load(load_image()), (200, 50))
            pygame.display.flip()
    pygame.time.Clock().tick(50)
