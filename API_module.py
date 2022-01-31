from geocoder_module import *


def get_map_params(response):
    toponym_longitude, toponym_latitude, width, height = get_geo_data(response)
    return {
        "ll": f'{toponym_longitude},{toponym_latitude}',
        "spn": f'{width},{height}',
        "l": "map",
        "size": '400,400'
    }


def load_map(response=None, map_params=None):
    import requests
    if map_params is None:
        if response is None:
            raise TypeError("Указано неверное количество параметров")
        map_params = get_map_params(response)
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    return requests.get(map_api_server, params=map_params)
