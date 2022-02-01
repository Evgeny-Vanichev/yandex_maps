import pygame
import sys
from io import BytesIO
from API_module import *


def load_image():
    # Получение картинки с координатами coords
    print(map_params)
    map_params['ll'] = f'{long},{lat}'
    map_params['spn'] = f'{spn},{spn}'
    map_response = load_map(map_params=map_params)
    return BytesIO(map_response.content)


# Получение координат объекта target
response = geocoder_request("Москва")
long, lat = get_geo_data(response, without_spn=True)
map_params = get_map_params(response)
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
            screen.blit(pygame.image.load(load_image()), (200, 50))
            pygame.display.flip()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 110 <= event.pos[0] <= 160 and 165 <= event.pos[1] <= 215:
                map_params['l'] = "sat"
            elif 110 <= event.pos[0] <= 160 and 265 <= event.pos[1] <= 315:
                map_params['l'] = "map"
            elif 110 <= event.pos[0] <= 160 and 365 <= event.pos[1] <= 415:
                map_params['l'] = "skl"
            screen.blit(pygame.image.load(load_image()), (200, 50))
            pygame.display.flip()
    pygame.time.Clock().tick(50)
