import json
import config


def parse_city_json(json_file='russia.json'):
    p_obj = None
    try:
        js_obj = open(json_file, "r", encoding="utf-8")
        p_obj = json.load(js_obj)
    except Exception as err:
        print(err)
        return None
    finally:
        js_obj.close()   
    return [city['city'].lower() for city in p_obj]

def get_city(city):
    normilize_city = city.strip().lower()
    if is_correct_city_name(normilize_city):
        if normilize_city[-1] in ('ь', 'ъ'):
            normilize_city = normilize_city[:-1]

        if get_city.previous_city != "" and normilize_city[0] != get_city.previous_city[-1]:
            return 'Город должен начинаться на "{0}"!🤓'.format(get_city.previous_city[-1])

        if normilize_city not in cities_already_named:
            cities_already_named.add(normilize_city)
            last_latter_city = normilize_city[-1]
            proposed_names = list(filter(lambda x: x[0] == last_latter_city, cities))
            if proposed_names:
                for city in proposed_names:
                    if city not in cities_already_named:
                        cities_already_named.add(city)
                        if city[-1] in ('ь', 'ъ'):
                            get_city.previous_city = city[:-1]
                        else:
                            get_city.previous_city = city
                        return city.capitalize()
            return winer()
        else:
            return 'Город уже был😝\nДавай другой🤓'
    else:
        return 'Не могу понять🧐\n❌Некорректное название города❌\nПопробуй ещё раз'

def winer():
    config.gameBool = False
    config.winerBool = True
    return 'Я не знаю города на эту букву😰\n🎉Ты выиграл🎉, поздравляю🥳'

get_city.previous_city = "" 

def is_correct_city_name(city):
    return city[-1].isalpha()

def refresh():
    get_city.previous_city = ""
    cities_already_named.clear()
    
cities = parse_city_json() # города которые знает бот
cities_already_named = set()  # города, которые уже называли