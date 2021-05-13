import json
import config
from sqlighter import SQLighter

class City_game():

    def __init__(self):
        """Добавляем словарь с сохранениями и списоком городов"""
        self.save_game = dict()
        self.cities = None

    def check_user(self, user_id):
        """Проверка наличия id в сохранениях"""
        return user_id in self.save_game

    def add_user(self, user_id):
        """Добавление user в словарь"""
        self.save_game[user_id] = ['', []]

    def parse_city_json(self, json_file='russia.json'): #перечитывание файла с городами
        """Заполняем список городов"""
        p_obj = None
        try:
            js_obj = open(json_file, "r", encoding="utf-8")
            p_obj = json.load(js_obj)
        except Exception as err:
            print(err)
            return None
        finally:
            js_obj.close()   
        self.cities = [city['city'].lower() for city in p_obj]

    def get_city(self, user_id, city):
        """Проверка ответа и прочее"""

        def is_correct_city_name(city):
            """Проверка последней буквы"""
            return city[-1].isalpha()

        def winer():
            config.winerBool = True
            return 'Я не знаю города на эту букву😰\n🎉Ты выиграл🎉, поздравляю🥳'

        self.cities_already_named = self.save_game[user_id][1]

        normilize_city = city.strip().lower()           #форматирование полученного города
        if is_correct_city_name(normilize_city):        #проверка на коррекцию города
            if normilize_city[-1] in ('ь', 'ъ', 'ы', 'й'):   #проверка последней буквы
                normilize_city = normilize_city[:-1]

            if self.save_game[user_id][0] != "" and normilize_city[0] != self.save_game[user_id][0][-1]:    #проверка первой буквы
                return 'Город должен начинаться на "{0}"!🤓'.format(self.save_game[user_id][0][-1])

            if normilize_city not in self.cities_already_named:      #проверка назывался ли город
                self.cities_already_named.append(normilize_city)        #добавление в список названых городов
                last_latter_city = normilize_city[-1]           
                proposed_names = list(filter(lambda x: x[0] == last_latter_city, self.cities)) #создание списка известных городов на последнюю букву
                if proposed_names:
                    for city in proposed_names:
                        if city not in self.cities_already_named:    #проверка назывался ли город
                            self.cities_already_named.append(city)      #добавление в список названых городов
                            if city[-1] in ('ь', 'ъ', 'ы', 'й'):
                                self.save_game[user_id][0] = city[:-1]
                            else:
                                self.save_game[user_id][0] = city
                            return city.capitalize()
                return winer()
            else:
                return 'Город уже был😝\nДавай другой🤓'
        else:
            return 'Не могу понять🧐\n❌Некорректное название города❌\nПопробуй ещё раз'

    def refresh(self, user_id):
        self.save_game[user_id][0] = ""
        self.save_game[user_id][1].clear()