import json
import config
from sqlighter import SQLighter

def parse_city_json(json_file='russia.json'): #перечитывание файла с городами
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
    normilize_city = city.strip().lower()           #форматирование полученного города
    if is_correct_city_name(normilize_city):        #проверка на коррекцию города
        if normilize_city[-1] in ('ь', 'ъ', 'ы'):   #проверка последней буквы
            normilize_city = normilize_city[:-1]

        if get_city.previous_city != "" and normilize_city[0] != get_city.previous_city[-1]:    #проверка первой буквы
            return 'Город должен начинаться на "{0}"!🤓'.format(get_city.previous_city[-1])

        if normilize_city not in cities_already_named:      #проверка назывался ли город
            cities_already_named.add(normilize_city)        #добавление в список названых городов
            last_latter_city = normilize_city[-1]           
            proposed_names = list(filter(lambda x: x[0] == last_latter_city, cities)) #создание списка известных городов на последнюю букву
            if proposed_names:
                for city in proposed_names:
                    if city not in cities_already_named:    #проверка назывался ли город
                        cities_already_named.add(city)      #добавление в список названых городов
                        if city[-1] in ('ь', 'ъ', 'ы'):
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