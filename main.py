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


# Получение координат объекта target
response = geocoder_request("Москва")
long, lat = get_geo_data(response, without_spn=True)
map_params = get_map_params(response)
spn = 0.3 / 4
pygame.init()
screen = pygame.display.set_mode((400, 400))
screen.blit(pygame.image.load(load_image()), (0, 0))
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
            screen.blit(pygame.image.load(load_image()), (0, 0))
            pygame.display.flip()
    pygame.time.Clock().tick(50)
