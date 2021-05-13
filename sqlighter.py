import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM subscriptions WHERE status = ?", [(status)]).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM subscriptions WHERE user_id = ?", [(user_id)]).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, username=None):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO subscriptions (user_id, username) VALUES(?,?)", (user_id, username))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE subscriptions SET status = ? WHERE user_id = ?", (status, user_id))

    def update_valuebool(self, user_id, boolname, valuebool):
        """Обновляем одину из логических переменных пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE subscriptions SET " + boolname + " = ? WHERE user_id = ?", (valuebool, user_id))

    def update_bool(self, user_id, boolname):
        """Обновляем одину из логических переменных пользователя выключая остальные"""
        with self.connection:
            self.cursor.execute("UPDATE subscriptions SET boboltyshkaBool = FALSE, helloBool = FALSE, menuBool = FALSE, gameBool = FALSE, connectionBool = FALSE, forwardMessage = FALSE, forwardSpam = FALSE, forwardOtvet = FALSE, adminBool = FALSE WHERE user_id = ?", [(user_id)])
            self.connection.commit()
            return self.cursor.execute("UPDATE subscriptions SET " + boolname + " = TRUE WHERE user_id = ?", [(user_id)])

    def check_bool(self, user_id, boolname):
        """Проверка статуса переменной"""
        with self.connection:
            result = self.cursor.execute("SELECT " + boolname + " FROM subscriptions WHERE user_id = ?", [(user_id)]).fetchall()
            return bool(result[0][0])

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()