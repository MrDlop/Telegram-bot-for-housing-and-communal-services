import time
import datetime
from datetime import datetime
import telebot
import pyautogui
import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import config

# connecting to google tables
url_text = 'https://www.googleapis.com/auth/spreadsheets'
url_text_1 = 'https://www.googleapis.com/auth/drive'
CREDENTIALS_FILE = 'config.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, [url_text, url_text_1])
httpAuth = credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http=httpAuth)
spreadsheetId = config.ID

# setting up work with google tables
gc = gspread.authorize(credentials)
sht1 = gc.open_by_key(config.ID)
worksheet = sht1.worksheet("Лист1")
wks = sht1.worksheet("1")
wdfs = sht1.worksheet("Лист2")
your_home = ((service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId,
                                                       ranges=["Лист1!I2:I240"],
                                                       valueRenderOption='FORMATTED_VALUE',
                                                       dateTimeRenderOption='FORMATTED_STRING').execute())[
    'valueRanges'][0]['values'])

# configuring the pyautogui module
screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()

# variables for working with counters
day = 23
day1 = 23
days = 0
days2 = '0'

# lines to make it easier to work with text output
mess1 = "Для начала выберите интересующую вас категорию:"
mess2 = "Для коректной работы функции, отправьте в сообщении показания счетчика за прошлый месяц"
mess3 = "Пришлите показания счетчика"
mess4 = "Показания счетчика приняты"
mess5 = "Выберите счетчик, показание которого вы хотите сдать:"
mess6 = "Теперь пришлите показания счетчика на данный момент"
mess7 = "Время прислать показания счетчиков, вы можете скинуть показания в течении "

# getting a token
bot = telebot.TeleBot(config.TOKEN)

# keyboards
poll_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
poll_board.row('Назад').add(
    'Опрос 1', 'Опрос 2', 'Опрос 3')

ask_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
ask_board.row('Фото').add('Отсутствует')

poll_1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
poll_1.row("Назад")

keyboard8 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard8.add('Отмена')

keyboard16 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard16.row('Счетчик электроэнергии')
keyboard16.add('Счетчик горячей воды')
keyboard16.add('Счетчик холодной воды')
keyboard16.add('Счетчик горячей воды(2)')
keyboard16.add('Счетчик холодной воды(2)')
keyboard16.add('Счетчик горячей воды(3)')
keyboard16.add('Счетчик газа')
keyboard16.add('Назад')

keyboard_qwe = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_qwe.add('Вернуться в меню')

keyboard_auto = telebot.types.ReplyKeyboardMarkup(True, True).row('Вход')

news_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
news_board.row('О предстоящем ремонте').add(
    'Результаты работ', 'Просьбы убрать авто и т.д.', 'Опросы', 'Назад')

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).row('❗️Оформить заявку о проблеме в АДС')
keyboard.add('📄 Справка', '📅 Новости').add('💬 Чат дома', 'Сдать показания счетчиков')

reference_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
reference_board.add('📃 Контактная информация').add('🏢 О доме', 'Об УК', 'Назад')

lui = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
lui.row('О предстоящем ремонте').add('Результаты работ',
                                     'Просьбы убрать авто и т.д.',
                                     'Опросы', 'Вернуться в меню')

hks_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
hks_board.add('Дальше', 'Вернуться в меню')

keyboard_mc = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_mc.row('Номера телефонов').add('График работы',
                                        'Прайс на дополнительные услуги',
                                        'Часы приема',
                                        'Назад')


# start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте, вы зашли в чат-бота от МойМКД.', reply_markup=keyboard_auto)


# commands for communication
@bot.message_handler(content_types=['text'])
def input_fullname(message):
    if message.text.lower() == 'вход':
        bot.send_message(message.from_user.id, 'Введите своё ФИО')
        bot.register_next_step_handler(message, input_cadastral_number)


def input_cadastral_number(message):
    send = bot.send_message(message.chat.id, 'Введите свой кадастровый номер')
    bot.register_next_step_handler(send, login, message.text)


def login(message, cadastral_number):
    if len(message.text) > 15:
        if not worksheet.findall(cadastral_number):
            bot.send_message(message.from_user.id, 'Неверный адрес или ФИО', reply_markup=keyboard_auto)
            bot.register_next_step_handler(message, input_fullname)
        else:
            cell = worksheet.find(cadastral_number)
            results = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId,
                                                               ranges=["Лист1!B2:B240"],
                                                               valueRenderOption='FORMATTED_VALUE',
                                                               dateTimeRenderOption='FORMATTED_STRING').execute()

            result = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId,
                                                              ranges=["Лист1!C%s" % cell.row],
                                                              valueRenderOption='FORMATTED_VALUE',
                                                              dateTimeRenderOption='FORMATTED_STRING').execute()
            if int(any(any(message.text in s for s in i) for i in results['valueRanges'][0]['values'])) == 1 and int(
                    any(any(cadastral_number in s for s in i) for i in result['valueRanges'][0]['values'])) == 1:
                service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": "Лист1!I%s:AA%s" % (cell.row, cell.row),
                         "majorDimension": "ROWS",
                         "values": [
                             [message.chat.id, (wks.find(worksheet.cell(cell.row, 1).value)).row, '0', '0',
                              message.text,
                              '0', '0', '0', '0', '0', '0', '0', '0', '0',
                              '0', '0', '0', '0', '0', ]]}
                    ]}).execute()
                bot.send_message(message.chat.id, "Напишите номер(если не хотите, введите 1)")
                bot.register_next_step_handler(message, phone, cell)
            else:
                bot.send_message(message.from_user.id, 'Неверный адрес или ФИО.', reply_markup=keyboard_auto)
                bot.register_next_step_handler(message, input_fullname)
    else:
        bot.send_message(message.from_user.id, 'Неверный адрес или ФИО.', reply_markup=keyboard_auto)
        bot.register_next_step_handler(message, input_fullname)


def phone(message, cell):
    service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "Лист1!L%s" % cell.row,
             "majorDimension": "ROWS",
             "values": [[message.text]]}
        ]}).execute()
    bot.send_message(message.chat.id, mess1, reply_markup=keyboard)
    bot.register_next_step_handler(message, menu)


# main
def menu(message):
    if message.text.lower() in ('сдать показания счетчиков',
                                '❗️оформить заявку о ',
                                'проблеме в адс',
                                '💬 чат дома',
                                '📅 новости',
                                '📄 справка'):
        if message.text.lower() == '📄 справка':
            bot.send_message(message.chat.id, "Выберите интересующую информацию", reply_markup=reference_board)
            bot.register_next_step_handler(message, reference)
        elif message.text.lower() == '📅 новости':
            bot.send_message(message.chat.id, "Выберите категорию запроса", reply_markup=news_board)
            bot.register_next_step_handler(message, news)
        elif message.text.lower() == '💬 чат дома':
            if wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 2).value == "":
                pyautogui.click(25, 47)  # menu
                time.sleep(0.5)
                pyautogui.click(128, 188)  # new group
                time.sleep(0.5)
                pyautogui.write(
                    str(wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 1).value),
                    interval=0.05)  # name
                pyautogui.click(614, 587)  # next
                time.sleep(0.1)
                pyautogui.click(489, 365)  # add member
                time.sleep(0.1)
                pyautogui.click(606, 804)  # invite via link
                time.sleep(0.1)
                pyautogui.moveTo(935, 47)
                time.sleep(0.3)
                pyautogui.click()  # settings
                time.sleep(0.5)
                pyautogui.click(851, 162)  # управление группой
                time.sleep(0.5)
                pyautogui.click(469, 689)  # admin
                time.sleep(0.5)
                pyautogui.click(420, 805)  # new admin
                time.sleep(0.5)
                pyautogui.click(474, 424)  # additional admin
                time.sleep(0.1)
                pyautogui.click(454, 578)  # добавление админов
                time.sleep(0.1)
                pyautogui.click(595, 939)  # сохранить
                time.sleep(0.3)
                pyautogui.click(606, 803)  # закрыть
                time.sleep(0.1)
                pyautogui.click(470, 539)  # тип группы
                time.sleep(0.1)
                pyautogui.click(359, 637)  # копировать ссылку
                time.sleep(0.1)
                pyautogui.click(417, 652)  # создать ссылку
                time.sleep(0.1)
                pyautogui.click(605, 571)  # ок
                time.sleep(0.1)
                pyautogui.click(376, 655)  # копировать ссылку
                time.sleep(0.1)
                pyautogui.click(594, 721)  # сохранить
                time.sleep(0.1)
                pyautogui.click(598, 827)  # сохранить
                time.sleep(0.1)
                pyautogui.click(1446, 806)  # клик
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.1)
                pyautogui.press('enter')  # переход на новую строку
                time.sleep(0.1)
                pyautogui.click(984, 562)  # файл
                time.sleep(0.1)
                pyautogui.click(1035, 647)  # сохранить
            house = wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 2).value
            house_but = telebot.types.InlineKeyboardButton(text='Чат дома', url=house)
            keyboard_house = telebot.types.InlineKeyboardMarkup().add(house_but)
            bot.send_message(message.chat.id, 'Для перехода нажмите на кнопку ниже', reply_markup=keyboard_house)
            bot.register_next_step_handler(message, menu)

        elif message.text.lower() == '❗️оформить заявку о проблеме в адс':
            bot.send_message(message.chat.id, "Подробно опишите проблему")
            bot.register_next_step_handler(message, edc_1)
        elif message.text.lower() == "сдать показания счетчиков":
            global day1, days, days2, day
            now = datetime.now()
            day_now = now.day
            if day_now == day:
                month = now.month
                year = now.year
                if month in (1, 3, 5, 7, 8, 10, 12):
                    days = 10
                    days2 = '10'
                elif month in (4, 6, 9, 11):
                    days = 9
                    days2 = '9'
                elif month == 2:
                    if year % 4 == 0:
                        days = 8
                        days2 = '8'
                    else:
                        days = 7
                        days2 = '7'
                bot.send_message(message.from_user.id, mess5,
                                 reply_markup=keyboard16)
                bot.register_next_step_handler(message, meter_reading)
            elif day_now == day1:
                bot.send_message(message.from_user.id, mess5,
                                 reply_markup=keyboard16)
                bot.register_next_step_handler(message, meter_reading)
            else:
                bot.send_message(message.from_user.id, "Эта функция работает только в дни сдачи показаний счетчиков!",
                                 reply_markup=keyboard_qwe)
                bot.register_next_step_handler(message, exit5)
    else:
        bot.register_next_step_handler(message, menu)


def edc_1(message):
    bot.send_message(config.worker, message.from_user.username)
    bot.send_message(config.worker, message.text)
    bot.send_message(message.chat.id, "Выберете в каком виде вы прикрепите доказательства", reply_markup=ask_board)
    bot.register_next_step_handler(message, eds_0)


def eds_0(message):
    if message.text.lower() in ('отсутствует', 'фото'):
        if message.text.lower() == 'фото':
            bot.send_message(message.chat.id, "Пришлите фото")
            bot.register_next_step_handler(message, eds_photo)
        elif message.text.lower() == 'отсутствует':
            bot.send_message(message.chat.id,
                             "Для устранения ложных вызовов мы просим вас добавить док-ва, используйте "
                             "данную функцию снова и прикрепите док-ва для того, что бы ваша заявка была"
                             " отправлена")
            bot.send_message(message.chat.id, mess1, reply_markup=keyboard)
            bot.register_next_step_handler(message, menu)
    else:
        bot.register_next_step_handler(message, eds_0)


def eds_photo(message):
    ant = message.photo[0].file_id
    bot.send_photo(config.worker, ant)
    bot.send_message(message.chat.id, "Ваша заявка была отправлена модератору")
    bot.send_message(message.chat.id, mess1, reply_markup=keyboard)
    bot.register_next_step_handler(message, menu)  # все можно исправить доп аргументом


def news(message):
    if message.text.lower() in ('о предстоящем ремонте',
                                'результаты работ',
                                'просьбы убрать авто и т.д.',
                                'опросы',
                                'назад'):
        if message.text.lower() == 'о предстоящем ремонте':
            bot.send_message(message.chat.id,
                             wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 4).value)
            bot.register_next_step_handler(message, news)
        elif message.text.lower() == 'результаты работ':
            bot.send_message(message.chat.id,
                             wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 5).value)
            bot.register_next_step_handler(message, news)
        elif message.text.lower() == 'просьбы убрать авто и т.д.':
            bot.send_message(message.chat.id,
                             wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 6).value)
            bot.register_next_step_handler(message, news)
        elif message.text.lower() == 'опросы':
            bot.send_message(message.chat.id, "Выберите опрос", reply_markup=poll_board)
            bot.register_next_step_handler(message, poll)
        elif message.text.lower() == 'назад':
            bot.send_message(message.chat.id, mess1, reply_markup=keyboard)
            bot.register_next_step_handler(message, menu)
    else:
        bot.register_next_step_handler(message, news)


# функции от meter_reading до gas_meter2 для работы со счетчиками
def meter_reading(message):
    if message.text.lower() in ('счетчик электроэнергии',
                                'счетчик горячей воды',
                                'счетчик холодной воды',
                                'счетчик горячей воды(2)',
                                'счетчик холодной воды(2)',
                                'счетчик горячей воды(3)',
                                'счетчик газа', 'назад'):
        if message.text.lower() == 'счетчик электроэнергии':
            meter_h(message, message.chat.id, 14, electricity_meter1)

        elif message.text.lower() == 'счетчик горячей воды':
            meter_h(message, message.chat.id, 15, hot_water_meter1)

        elif message.text.lower() == 'счетчик холодной воды':
            meter_h(message, message.chat.id, 16, cold_water_meter1)

        elif message.text.lower() == 'счетчик горячей воды(2)':
            meter_h(message, message.chat.id, 17, hot_water2_meter1)

        elif message.text.lower() == 'счетчик холодной воды(2)':
            meter_h(message, message.chat.id, 18, cold_water2_meter1)

        elif message.text.lower() == 'счетчик горячей воды(3)':
            meter_h(message, message.chat.id, 19, hot_water3_meter1)

        elif message.text.lower() == 'счетчик газа':
            meter_h(message, message.chat.id, 20, gas_meter1)

        elif message.text.lower() == 'назад':
            bot.send_message(message.chat.id, mess1, reply_markup=keyboard)
            bot.register_next_step_handler(message, menu)
    else:
        bot.register_next_step_handler(message, meter_reading)


def exit5(message):
    if message.text.lower() == 'вернуться в меню':
        bot.send_message(message.from_user.id, mess1,
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, menu)
    elif message.text.lower() != 'вернуться в меню':
        bot.register_next_step_handler(message, exit5)


def electricity_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 16, 23, electricity_meter2)


def electricity_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 23, 3.5)


def hot_water_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 18, 25, hot_water_meter2)


def hot_water_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 25, 127.48)


def cold_water_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 14, 21, cold_water_meter2)


def cold_water_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 21, 13.92)


def hot_water2_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 19, 26, hot_water2_meter2)


def hot_water2_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 26, 127.48)


def cold_water2_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 15, 22, cold_water2_meter2)


def cold_water2_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 22, 13.92)


def hot_water3_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 20, 27, hot_water3_meter2)


def hot_water3_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 27, 127.48)


def gas_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 17, 24, gas_meter2)


def gas_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 24, 6.31)


def meter_h(message, id_user, str_A, f2):
    word1, word2 = "осталось", "дней"
    if days == 1:
        word1, word2 = "остался", "день"
    elif days == 2 or days == 3 or days == 4:
        word1, word2 = "осталось", "дня"
    bot.send_message(id_user, f"У вас {word1} {days2} {word2}", reply_markup=keyboard8)
    if worksheet.cell(worksheet.find(str(id_user)).row, str_A).value == 0:
        bot.send_message(id_user, mess2)
    else:
        bot.send_message(id_user, mess3)
    bot.register_next_step_handler(message, f2)


def meters_h(message, id_user, friId, text, str_A, str_B, f2):
    if message.text.lower() == 'отмена':
        bot.send_message(friId, mess5,
                         reply_markup=keyboard16)
        bot.register_next_step_handler(message, meter_reading)
    elif message.text.lower() != 'отмена':
        if int(worksheet.cell(worksheet.find(str(id_user)).row, str_A).value) == 0:
            worksheet.update_cell(worksheet.find(str(id_user)).row, str_B, text)
            worksheet.update_cell(worksheet.find(str(id_user)).row, str_A, '1')
            bot.send_message(friId, mess6)
            bot.register_next_step_handler(message, f2)
        elif message.text:
            worksheet.update_cell(worksheet.find(str(id_user)).row, str_B,
                                  worksheet.cell(worksheet.find(str(id_user)).row,
                                                 str_B).value + '/' + text)
            bot.send_message(friId, mess4, reply_markup=keyboard_qwe)
            bot.register_next_step_handler(message, exit5)


def meters_h2(message, friId, id_user, text, str_A, n):
    if text:
        worksheet.update_cell(worksheet.find(str(id_user)).row, str_A,
                              worksheet.cell(worksheet.find(str(id_user)).row, str_A).value + '|' + text)
        bot.send_message(friId, mess4, reply_markup=keyboard_qwe)

        money = worksheet.cell(worksheet.find(str(id_user)).row, str_A).value.split("|")
        c = (int(money[1]) - int(money[0])) * n
        bot.send_message(friId, f"Вам нужно заплатить {c} рублей", reply_markup=keyboard_qwe)
        bot.register_next_step_handler(message, exit5)


def reference(message):
    if message.text.lower() in ('🏢 о доме',
                                '📃 контактная информация',
                                'об ук',
                                'назад'):
        if message.text.lower() == '🏢 о доме':
            bot.send_message(message.chat.id,
                             wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 3).value)
            bot.register_next_step_handler(message, reference)
        elif message.text.lower() == '📃 контактная информация':
            bot.send_message(message.chat.id, 'Выберите подкатегорию', reply_markup=keyboard_mc)
            bot.register_next_step_handler(message, mc)
        elif message.text.lower() == 'об ук':
            bot.send_message(message.chat.id, wdfs.cell(
                wdfs.find(wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 8).value).row,
                6).value)
            bot.register_next_step_handler(message, reference)
        elif message.text.lower() == 'назад':
            bot.send_message(message.chat.id, mess1, reply_markup=keyboard)
            bot.register_next_step_handler(message, menu)
    else:
        bot.register_next_step_handler(message, reference)


def mc(message):
    if message.text.lower() in ('номера телефонов',
                                'график работы',
                                'прайс на дополнительные услуги',
                                'часы приема',
                                'назад'):
        if message.text.lower() == 'номера телефонов':
            bot.send_message(message.chat.id, wdfs.cell(
                wdfs.find(wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 8).value).row,
                2).value)
            bot.register_next_step_handler(message, mc)
        elif message.text.lower() == 'график работы':
            bot.send_message(message.chat.id, wdfs.cell(
                wdfs.find(wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 8).value).row,
                3).value)
            bot.register_next_step_handler(message, mc)
        elif message.text.lower() == 'прайс на дополнительные услуги':
            bot.send_message(message.chat.id, wdfs.cell(
                wdfs.find(wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 8).value).row,
                4).value)
            bot.register_next_step_handler(message, mc)
        elif message.text.lower() == 'часы приема':
            bot.send_message(message.chat.id, wdfs.cell(
                wdfs.find(wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 8).value).row,
                5).value)
            bot.register_next_step_handler(message, mc)
        elif message.text.lower() == 'назад':
            bot.send_message(message.chat.id, "Выберите интересующую информацию", reply_markup=reference_board)
            bot.register_next_step_handler(message, reference)
    else:
        bot.register_next_step_handler(message, mc)


def poll(message):
    if message.text.lower() in ('опрос 1', 'опрос 2', 'опрос 3', 'назад'):
        if message.text.lower() == 'опрос 1':
            question = wks.cell(wks.find('опрос1').row, 14).value
            opti = wks.row_values(wks.find('опрос1').row)
            del opti[0:15]
            bot.send_message(message.chat.id, str(question) + '\nВарианты Ответов\n' + "\n".join(opti),
                             reply_markup=poll_1)
            bot.register_next_step_handler(message, poll1)
        elif message.text.lower() == 'опрос 2':
            question = wks.cell(wks.find('опрос2').row, 14).value
            opti = wks.row_values(wks.find('опрос2').row)
            del opti[0:15]
            bot.send_message(message.chat.id, str(question) + '\nВарианты Ответов\n' + "\n".join(opti),
                             reply_markup=poll_1)
            bot.register_next_step_handler(message, poll2)

        elif message.text.lower() == 'опрос 3':
            question = wks.cell(wks.find('опрос3').row, 14).value
            opti = wks.row_values(wks.find('опрос3').row)
            del opti[0:15]
            bot.send_message(message.chat.id, str(question) + '\nВарианты Ответов\n' + "\n".join(opti),
                             reply_markup=poll_1)
            bot.register_next_step_handler(message, poll3)
        elif message.text.lower() == 'назад':
            bot.send_message(message.chat.id, "Выберите категорию запроса", reply_markup=news_board)
            bot.register_next_step_handler(message, news)
    else:
        bot.register_next_step_handler(message, poll)


def poll1(message):
    poll_all(message, message.text, message.chat.id, poll1, 'опрос1')


def poll2(message):
    poll_all(message, message.text, message.chat.id, poll2, 'опрос2')


def poll3(message):
    poll_all(message, message.text, message.chat.id, poll3, 'опрос3')


def poll_all(message, text, id_user, function, txt):
    opti = wks.row_values(wks.find(txt).row)
    del opti[0:15]
    if opti.count(text) == 1:
        wks.update_cell(int(wks.find(txt).row + 1), int(opti.index(text) + 16),
                        int(wks.cell(wks.find(txt).row + 1, opti.index(text) + 16).value) + 1)
        bot.send_message(id_user, "Выберите опрос", reply_markup=poll_board)
        bot.register_next_step_handler(message, poll)
    elif message.text.lower() == 'назад':
        bot.send_message(id_user, "Выберите опрос", reply_markup=poll_board)
        bot.register_next_step_handler(message, poll)
    elif message.text.lower() != 'назад' and opti.count(text) != 1:
        bot.register_next_step_handler(message, function)


bot.polling()
