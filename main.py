import os
import pygame
import requests
import sys


def load_image():
    # Получение картинки с координатами coords
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={coords[0]},{coords[1]}&spn={zoom}," \
                  f"{zoom}&size=500,400&l=map"
    response = requests.get(map_request)
    if not response:
        print("Простите, возникла непредвиденная ошибка")
        sys.exit()
    with open(map_file, 'wb') as file:
        file.write(response.content)


def get_coords(target):
    coords_request = f"https://geocode-maps.yandex.ru/1.x/" \
                     f"?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json&geocode={target}"
    response = requests.get(coords_request)
    if not response:
        print("Простите, возникла непредвиденная ошибка")
        sys.exit()
    return [float(x) for x in
            response.json()["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]["Point"]["pos"].split()]


# Получение координат объекта target
coords = get_coords('Москва')
map_file = "map.png"
zoom = 0.3
load_image()
pygame.init()
screen = pygame.display.set_mode((500, 400))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            os.remove(map_file)
            sys.exit()
    pygame.time.Clock().tick(50)
