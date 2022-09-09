import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup


class Valut_dollar:
    # url адрес нужной страницы
    Dollar_rub = 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%' \
                 'D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0' \
                 '%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80&aqs=chrome.0.0i131i433i512j69i57' \
                 'j0i131i433i512l3j0i512l2j0i131i433i512j0i512l2.2920j1j7&sourceid=chrome&ie=UTF-8'
    Euro_rub = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%D0%B2%D' \
               '1%80%D0%BE&rlz=1C1PNBB_enRU991RU991&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%' \
               'D0%B2%D1%80%D0%BE&aqs=chrome..69i57j0i131i433i512l8j0i512.2410j1j7&sourceid=chrome&ie=UTF-8'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }
    # словарь с заголовами, описывающими пользователя, что переходит по url адресу(иначе будет считаться, что пытается зайти бот)

    def get_dollar_price(self):
        #Метод, возвращающий курс доллара, на вход ничего не подается
        full_page = requests.get(self.Dollar_rub, headers=self.headers) #запрос по нужному url
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll( #выборка элементов с сайта(парсинг)
            "span", {
                "class": "DFlfde",
                "class": "SwHCTb",
                "data-precision": 2
            })
        return convert[0].text #возвращение курса доллара в формате текста

    def get_euro_price(self):
        #Метод, возвращающий курс евро, на вход ничего не подается
        full_page = requests.get(self.Euro_rub, headers=self.headers) #запрос по нужному url
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll( #выборка элементов с сайта(парсинг)
            "span", {
                "class": "DFlfde",
                "class": "SwHCTb",
                "data-precision": 2
            })
        return convert[0].text #возвращение курса евро в формате текста

bot = telebot.TeleBot('5247559952:AAFiDtHaL2enmi91Uyw_0wRhOg5WR8EDFZs') #Передача токена нашего бота

@bot.message_handler(commands=['start'])
def start(message):
    #Функция, описывающая команду "start", на вход подается сообщение пользователя
    name = f'Здравствуйте, <b><u>' \
           f'{message.from_user.first_name} {message.from_user.last_name}' \
           f'</u></b>, давайте же начнем'
    bot.send_message(message.chat.id, name, parse_mode='html') #Отправка сообщения пользователю
    bot.send_message(message.chat.id, "Введите команду /help", parse_mode='html') #Подсказка для пользователя

@bot.message_handler(commands=['help'])
def help(message):
    # Функция, описывающая команду "help", на вход подается сообщение пользователя
    markup = types.ReplyKeyboardMarkup() #Объявление объекта для создания кнопок
    dollar = types.KeyboardButton('Курс доллара') #Создание кнопки
    euro = types.KeyboardButton('Курс евро') #Создание кнопки
    start = types.KeyboardButton('/start') #Создание кнопки
    privet = types.KeyboardButton('Привет') #Создание кнопки
    markup.add(dollar, start, euro, privet) #Добавление кнопок
    bot.send_message(message.chat.id, 'Выберите нужную вам команду', reply_markup=markup)

@bot.message_handler()
def get_user_text(message):
    # Функция, описывающая действия, если пользователь прислал текст, а не команду, на вход подается сообщение пользователя
    if message.text == "Привет" or  message.text == "Здравствуйте" or  message.text == "Здравствуй":
        bot.send_message(message.chat.id,
                         "И вас категорически приветствую",
                         parse_mode='html')
    elif message.text == "Курс доллара" or message.text == "Dollar":
        valut = Valut_dollar() #Создание объекта класса Valut_dollar()
        bot.send_message(message.chat.id, valut.get_dollar_price(), parse_mode='html') #отправка сообщения пользователю, в котором содержится курс доллара
    elif message.text == "Курс евро" or message.text == "Euro":
        valut = Valut_dollar() #Создание объекта класса Valut_dollar()
        bot.send_message(message.chat.id, valut.get_euro_price(), parse_mode='html') #отправка сообщения пользователю, в котором содержится курс евро
    else: #в случае некорректного сообщения
        bot.send_message(message.chat.id,
                         "Я не понимаю вас. Попробуйте ввести нужную команду",
                         parse_mode='html')

bot.polling(none_stop=True) #постоянная работа бота

