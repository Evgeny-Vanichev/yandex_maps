def geocoder_request(target):
    import requests
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": target,
        "format": "json"}
    return requests.get(geocoder_api_server, params=geocoder_params)


def get_toponym(response):
    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    return json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


def get_left_right_corner(response=None, toponym=None):
    if response is not None:
        toponym = get_toponym(response)
    elif toponym is None:
        raise TypeError("Укажите хотя бы один из аргументов")
    l_corner, r_corner = [[float(i) for i in x.split(' ')]
                          for x in toponym["boundedBy"]["Envelope"].values()]
    return l_corner, r_corner


def get_spn(response=None, toponym=None, l_r_corner=None):
    if response is not None:
        toponym = get_toponym(response)
        l_r_corner = get_left_right_corner(toponym=toponym)
    elif toponym is not None:
        l_r_corner = get_left_right_corner(toponym=toponym)
    elif l_r_corner is None:
        raise TypeError("Укажите хотя бы один из аргументов")
    return (l_r_corner[1][i] - l_r_corner[0][i] for i in range(2))


def get_geo_data(response, without_spn=False):
    toponym = get_toponym(response)
    # Координаты центра топонима:
    lat, long = [float(x) for x in toponym["Point"]["pos"].split(" ")]
    if without_spn:
        return lat, long
    return lat, long, *get_spn(toponym=toponym)
