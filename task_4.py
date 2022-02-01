import os

import pygame
import requests


def load_file(response_content):
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response_content)
    file.close()
    return map_file


def geocode_request(delta_x, delta_y, l):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode" \
                       "=Москва&format=json"
    geo_response = requests.get(geocoder_request)
    jsn = geo_response.json()

    longitude, latitude = jsn["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point'][
        'pos'].split()
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}&spn={delta_x},{delta_y}&l={l}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return -1
    return load_file(response.content)


l = "map"
delta_x = 0.1
delta_y = 0.1
pygame.init()
screen = pygame.display.set_mode((1000, 600))
screen.fill((255, 255, 255))

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

screen.blit(pygame.image.load(geocode_request(delta_x, delta_y, l)), (200, 50))
pygame.display.flip()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                delta_x *= 2
                delta_y *= 2
            if event.key == pygame.K_PAGEUP:
                if delta_x > 0.001 and delta_y > 0.001:
                    delta_x /= 2
                    delta_y /= 2
            screen.blit(pygame.image.load(geocode_request(delta_x, delta_y, l)), (200, 50))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 110 <= event.pos[0] <= 160 and 165 <= event.pos[1] <= 215:
                l = "sat"
            elif 110 <= event.pos[0] <= 160 and 265 <= event.pos[1] <= 315:
                l = "map"
            elif 110 <= event.pos[0] <= 160 and 365 <= event.pos[1] <= 415:
                l = "skl"
            screen.blit(pygame.image.load(geocode_request(delta_x, delta_y, l)), (200, 50))

    pygame.display.flip()
pygame.quit()
os.remove("map.png")
