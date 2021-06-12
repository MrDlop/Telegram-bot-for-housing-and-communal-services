import telebot
import config
import time
import datetime
from datetime import datetime
import pyautogui
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import gspread

url_text = 'https://www.googleapis.com/auth/spreadsheets'
url_text_1 = 'https://www.googleapis.com/auth/drive'
CREDENTIALS_FILE = 'config.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, [url_text, url_text_1])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
spreadsheetId = config.ID

gc = gspread.authorize(credentials)
sht1 = gc.open_by_key(config.ID)
worksheet = sht1.worksheet("Лист1")
wks = sht1.worksheet("1")
wdfs = sht1.worksheet("Лист2")
# настройка модуля pyautogui по экран
screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()

day = 21
day1 = 22
days = 0
days2 = ''
a = 0
# строки для упрощения работы с выводом текста
mess1 = "Для начала выберите интересующую вас категорию:"
mess2 = "Для коректной работы функции, отправьте в сообщении показания счетчика за прошлый месяц"
mess3 = "Пришлите показания счетчика"
mess4 = "Показания счетчика приняты"
mess5 = "Выберите счетчик, показание которого вы хотите сдать:"
mess6 = "Теперь пришлите показания счетчика на данный момент1"
pop = "Время прислать показания счетчиков, вы можете скинуть показания в течении "

bot = telebot.TeleBot(config.TOKEN)
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
keyboard.add('📄 Справка', '📅 Новости')
keyboard.add('💬 Чат дома', 'Сдать показания счетчиков')
reference_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
reference_board.add('📃 Контактная информация')
reference_board.add('🏢 О доме', 'Об УК', 'Назад')
lui = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
lui.row('О предстоящем ремонте')
lui.add('Результаты работ',
        'Просьбы убрать авто и т.д.',
        'Опросы', 'Вернуться в меню')
hks_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
hks_board.add('Дальше', 'Вернуться в меню')
keyboard_mc = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_mc.row('Номера телефонов').add('График работы',
                                        'Прайс на дополнительные услуги',
                                        'Часы приема',
                                        'Назад')

your_home = ((service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId,
                                                       ranges=["Лист1!I2:I240"],
                                                       valueRenderOption='FORMATTED_VALUE',
                                                       dateTimeRenderOption='FORMATTED_STRING').execute())[
    'valueRanges'][0]['values'])


@bot.message_handler(commands=['start'])
# Сообщение о том, что вы начали использовать бота
def start_message(message):
    bot.send_message(message.chat.id, 'Здравствуйте, вы зашли в чат-бота от МойМКД.', reply_markup=keyboard_auto)


@bot.message_handler(content_types=['text'])
def manul(message):
    if message.text.lower() == 'вход':
        bot.send_message(message.from_user.id, 'Введите своё ФИО')
        bot.register_next_step_handler(message, two_q)


def two_q(message):
    global answers
    answers = [message.text]
    send = bot.send_message(message.chat.id, 'Введите свой кадастровый номер')
    bot.register_next_step_handler(send, three_q)


def three_q(message):
    answers.append(message.text)
    if len(answers[1]) > 15:
        if not worksheet.findall(answers[0]):
            bot.send_message(message.from_user.id, 'Неверный адрес или ФИО.', reply_markup=keyboard_auto)
            bot.register_next_step_handler(message, two_q)
        else:
            global cell
            cell = worksheet.find(answers[0])
            results = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId,
                                                               ranges=["Лист1!B2:B240"],
                                                               valueRenderOption='FORMATTED_VALUE',
                                                               dateTimeRenderOption='FORMATTED_STRING').execute()

            result = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId,
                                                              ranges=["Лист1!C%s" % cell.row],
                                                              valueRenderOption='FORMATTED_VALUE',
                                                              dateTimeRenderOption='FORMATTED_STRING').execute()
            if int(any(any(answers[1] in s for s in i) for i in results['valueRanges'][0]['values'])) == 1 and int(
                    any(any(answers[0] in s for s in i) for i in result['valueRanges'][0]['values'])) == 1:
                service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": "Лист1!I%s:AA%s" % (cell.row, cell.row),
                         "majorDimension": "ROWS",
                         "values": [
                             [message.chat.id, (wks.find(worksheet.cell(cell.row, 1).value)).row, '0', '0', answers[1],
                              '0', '0', '0', '0', '0', '0', '0', '0', '0',
                              '0', '0', '0', '0', '0', ]]}
                    ]}).execute()
                bot.send_message(message.chat.id, "Напишите номер(если не хотите, введите 1)")
                bot.register_next_step_handler(message, phone)
            else:
                bot.send_message(message.from_user.id, 'Неверный адрес или ФИО.', reply_markup=keyboard_auto)
                bot.register_next_step_handler(message, manul)
    else:
        bot.send_message(message.from_user.id, 'Неверный адрес или ФИО.', reply_markup=keyboard_auto)
        bot.register_next_step_handler(message, manul)


def phone(message):
    answers.append(message.text)

    service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "Лист1!L%s" % cell.row,
             "majorDimension": "ROWS",
             "values": [[answers[2]]]}
        ]}).execute()
    bot.send_message(message.chat.id, mess1, reply_markup=keyboard)
    bot.register_next_step_handler(message, menu)


def menu(message):
    global a
    global day1
    global days
    if message.text.lower() == '📄 справка':
        bot.send_message(message.chat.id, "Выберите интересующую информацию", reply_markup=reference_board)
        bot.register_next_step_handler(message, reference)
    elif message.text.lower() == '/hks_sch':
        bot.register_next_step_handler(message, hks_sch_message)
    elif message.text.lower() == '📅 новости':
        bot.send_message(message.chat.id, "Выберите категорию запроса", reply_markup=news_board)
        bot.register_next_step_handler(message, news)
    elif message.text.lower() == '💬 чат дома':
        user_hocha = wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 2).value
        if user_hocha != "":
            hocha = wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 2).value
            hocha_but = telebot.types.InlineKeyboardButton(text='Чат дома', url=hocha)
            keyboard_hocha = telebot.types.InlineKeyboardMarkup().add(hocha_but)
            bot.send_message(message.chat.id, 'Для перехода нажмите на кнопку ниже', reply_markup=keyboard_hocha)
            bot.register_next_step_handler(message, menu)
        elif user_hocha == "":
            # Создание чата
            pyautogui.click(25, 47)  # меню
            time.sleep(0.5)
            pyautogui.click(128, 188)  # создать группу
            time.sleep(0.5)
            pyautogui.write(str(wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 1).value),
                            interval=0.05)  # название
            pyautogui.click(614, 587)  # далее
            time.sleep(0.1)
            pyautogui.click(489, 365)  # доп. пользователь
            time.sleep(0.1)
            pyautogui.click(606, 804)  # создать
            time.sleep(0.1)
            pyautogui.moveTo(935, 47)
            time.sleep(0.3)
            pyautogui.click()  # настройки
            time.sleep(0.5)
            pyautogui.click(851, 162)  # управление группой
            time.sleep(0.5)
            pyautogui.click(469, 689)  # админы
            time.sleep(0.5)
            pyautogui.click(420, 805)  # добавить админа
            time.sleep(0.5)
            pyautogui.click(474, 424)  # доп. админ
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
            # Отправка ссылки на чат
            hocha_1 = wks.cell(worksheet.cell(worksheet.find(str(message.chat.id)).row, 10).value, 2).value
            hocha_but = telebot.types.InlineKeyboardButton(text='Чат дома', url=hocha_1)
            keyboard_hocha = telebot.types.InlineKeyboardMarkup().add(hocha_but)
            bot.send_message(message.chat.id, 'Для перехода нажмите на кнопку ниже', reply_markup=keyboard_hocha)
            bot.register_next_step_handler(message, menu)

    elif message.text.lower() == '❗️оформить заявку о проблеме в адс':
        bot.send_message(message.chat.id, "Подробно опишите проблему")
        bot.register_next_step_handler(message, ads_1)
    elif message.text.lower() == "сдать показания счетчиков":
        now = datetime.now()
        day_now = now.day
        if day_now == day:
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
    elif message.text.lower() != "сдать показания счетчиков" and message.text.lower() != '❗️оформить заявку о ' \
                                                                                         'проблеме в адс' and \
            message.text.lower() != '💬 чат дома' and message.text.lower() != '📅 новости' and message.text.lower() \
            != '📄 справка' and message.text.lower() != '📄 справка':
        bot.register_next_step_handler(message, menu)


# Функция для включения/выключения возможности сдачи показания счетчиков
def hks_sch_message(message):
    global a
    if a == 1:
        a = 0
        bot.send_message(message.from_user.id, "Выключено")
        bot.register_next_step_handler(message, menu)
    else:
        bot.send_message(message.from_user.id, "Включено")
        bot.register_next_step_handler(message, meters)
        bot.register_next_step_handler(message, menu)


def ads_1(message):
    bot.send_message(config.worker, message.from_user.username)
    bot.send_message(config.worker, message.text)
    bot.send_message(message.chat.id, "Выберете в каком виде вы прикрепите доказательства", reply_markup=ask_board)
    bot.register_next_step_handler(message, adc_0)


def adc_0(message):
    if message.text.lower() == 'фото':
        bot.send_message(message.chat.id, "Пришлите фото")
        bot.register_next_step_handler(message, adc_photo)
    elif message.text.lower() == 'отсутствует':
        bot.send_message(message.chat.id, "Для устранения ложных вызовов мы просим вас добавить док-ва, используйте "
                                          "данную функцию снова и прикрепите док-ва для того, что бы ваша заявка была"
                                          " отправлена")
        bot.send_message(message.chat.id, mess1, reply_markup=keyboard)
        bot.register_next_step_handler(message, menu)
    elif message.text.lower() != 'отсутствует' and message.text.lower() != 'фото':
        bot.register_next_step_handler(message, adc_0)


def adc_photo(message):
    ant = message.photo[0].file_id
    bot.send_photo(config.worker, ant)
    bot.send_message(message.chat.id, "Ваша заявка была отправлена модератору")
    bot.send_message(message.chat.id, mess1, reply_markup=keyboard)
    bot.register_next_step_handler(message, menu)  # все можно исправить доп аргументом


def news(message):
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
    elif message.text.lower() != 'о предстоящем ремонте' and message.text.lower() != 'результаты работ' and \
            message.text.lower() != 'просьбы убрать авто и т.д.' and \
            message.text.lower() != 'опросы' and message.text.lower() != 'назад':
        bot.register_next_step_handler(message, news)


# функции от meter_reading до gas_meter2 для работы со счетчиками
def meter_reading(message):
    global b1
    global a0
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

    elif message.text.lower() != 'счетчик электроэнергии' and message.text.lower() != 'счетчик горячей воды' and \
            message.text.lower() != 'счетчик холодной воды' and message.text.lower() != 'счетчик горячей воды(2)' and \
            message.text.lower() != 'счетчик холодной воды(2)' and \
            message.text.lower() != 'счетчик горячей воды(3)' and \
            message.text.lower() != 'счетчик газа' and message.text.lower() != 'назад':
        bot.register_next_step_handler(message, meter_reading)


def exit5(message):
    if message.text.lower() == 'вернуться в меню':
        bot.send_message(message.from_user.id, mess1,
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, menu)
    elif message.text.lower() != 'вернуться в меню':
        bot.register_next_step_handler(message, exit5)


def meters(message):
    global day1
    global days
    global days2
    global day
    global a
    a += 1
    while True:
        now = datetime.now()
        month = now.month
        year = now.year
        day_now = now.day
        if a == 2:
            a = 0
            break
        if day_now == day:
            if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
                days = 10
                days2 = '10'
            elif month == 4 or month == 6 or month == 9 or month == 11:
                days = 9
                days2 = '9'
            elif month == 2:
                if year % 4 == 0:
                    days = 8
                    days2 = '8'
                else:
                    days = 7
                    days2 = '7'
            opo = 0

            for user in str(your_home[opo]).replace("['", '').replace("']", ''):
                opo += opo
                print(user)
                bot.send_message(user, pop + days2 + "дней",
                                 reply_markup=keyboard)
            days -= 1
            day1 += 1
            time.sleep(86400)
        elif day_now == day1:
            day1 += 1
            if days == 0:
                for user in your_home:
                    bot.send_message(user, "Время приёма показаний счетчиков закончилось",
                                     reply_markup=keyboard_qwe)
                day1 = 22
                bot.register_next_step_handler(message, exit5)
                time.sleep(86400)
            else:
                days -= 1
            time.sleep(86400)


def electricity_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 16, 23, electricity_meter2)


def electricity_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 23)


def hot_water_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 18, 25, hot_water_meter2)


def hot_water_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 25)


def cold_water_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 14, 21, cold_water_meter2)


def cold_water_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 21)


def hot_water2_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 19, 26, hot_water2_meter2)


def hot_water2_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 26)


def cold_water2_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 15, 22, cold_water2_meter2)


def cold_water2_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 22)


def hot_water3_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 20, 27, hot_water3_meter2)


def hot_water3_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 27)


def gas_meter1(message):
    meters_h(message, message.chat.id, message.from_user.id, message.text, 17, 24, gas_meter2)


def gas_meter2(message):
    meters_h2(message, message.from_user.id, message.chat.id, message.text, 24)


def meter_h(message, id, str_A, f2):
    if days == 1:
        bot.send_message(message.chat.id, "У вас остался " + days2 + " день", reply_markup=keyboard8)
        if worksheet.cell(worksheet.find(str(id)).row, str_A).value == 0:
            bot.send_message(id, mess2)
            bot.register_next_step_handler(message, f2)
        else:
            bot.send_message(id, mess3)
            bot.register_next_step_handler(message, f2)
    else:
        bot.send_message(id, "У вас осталось " + days2 + " дней", reply_markup=keyboard8)
        if worksheet.cell(worksheet.find(str(id)).row, str_A).value == 0:
            bot.send_message(id, mess2)
            bot.register_next_step_handler(message, f2)
        else:
            bot.send_message(id, mess3)
            bot.register_next_step_handler(message, f2)


def meters_h(message, id, friId, text, str_A, str_B, f2):
    if message.text.lower() == 'отмена':
        bot.send_message(friId, mess5,
                         reply_markup=keyboard16)
        bot.register_next_step_handler(message, meter_reading)
    elif message.text.lower() != 'отмена':
        if int(worksheet.cell(worksheet.find(str(id)).row, str_A).value) == 0:
            worksheet.update_cell(worksheet.find(str(id)).row, str_B, text)
            worksheet.update_cell(worksheet.find(str(id)).row, str_A, '1')
            bot.send_message(friId, mess6)
            bot.register_next_step_handler(message, f2)
        elif message.text:
            worksheet.update_cell(worksheet.find(str(id)).row, str_B,
                                  worksheet.cell(worksheet.find(str(id)).row,
                                                 str_B).value + '/' + text)
            bot.send_message(friId, mess4, reply_markup=keyboard_qwe)
            bot.register_next_step_handler(message, exit5)


def meters_h2(message, friId, id, text, str_A):
    if text:
        worksheet.update_cell(worksheet.find(str(id)).row, str_A,
                              worksheet.cell(worksheet.find(str(id)).row, str_A).value + '|' + text)
        bot.send_message(friId, mess4, reply_markup=keyboard_qwe)
        bot.register_next_step_handler(message, exit5)


def reference(message):
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
    elif message.text.lower() != '🏢 о доме' and message.text.lower() != '📃 контактная информация' and \
            message.text.lower() != 'об ук' and message.text.lower() != 'назад':
        bot.register_next_step_handler(message, reference)


def mc(message):
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
    elif message.text.lower() != 'номера телефонов' and message.text.lower() != 'график работы' and \
            message.text.lower() != 'прайс на дополнительные услуги' and \
            message.text.lower() != 'часы приема' and message.text.lower() != 'назад':
        bot.register_next_step_handler(message, mc)


def poll(message):
    if message.text.lower() == 'опрос 1':
        question = wks.cell(wks.find('опрос1').row, 14).value
        opti = wks.row_values(wks.find('опрос1').row)
        del opti[0:15]
        bot.send_message(message.chat.id, str(question) + '\nВарианты Ответов\n' + "\n".join(opti), reply_markup=poll_1)
        bot.register_next_step_handler(message, poll1)
    elif message.text.lower() == 'опрос 2':
        question = wks.cell(wks.find('опрос2').row, 14).value
        opti = wks.row_values(wks.find('опрос2').row)
        del opti[0:15]
        bot.send_message(message.chat.id, str(question) + '\nВарианты Ответов\n' + "\n".join(opti), reply_markup=poll_1)
        bot.register_next_step_handler(message, poll2)

    elif message.text.lower() == 'опрос 3':
        question = wks.cell(wks.find('опрос3').row, 14).value
        opti = wks.row_values(wks.find('опрос3').row)
        del opti[0:15]
        bot.send_message(message.chat.id, str(question) + '\nВарианты Ответов\n' + "\n".join(opti), reply_markup=poll_1)
        bot.register_next_step_handler(message, poll3)
    elif message.text.lower() == 'назад':
        bot.send_message(message.chat.id, "Выберите категорию запроса", reply_markup=news_board)
        bot.register_next_step_handler(message, news)
    elif message.text.lower() != 'опрос 1' and message.text.lower() != 'опрос 2' and \
            message.text.lower() != 'опрос 3' and \
            message.text.lower() != 'назад':
        bot.register_next_step_handler(message, poll)


def poll1(message):
    poll_all(message, message.text, message.chat.id, poll1, 'опрос1')


def poll2(message):
    poll_all(message, message.text, message.chat.id, poll2, 'опрос2')


def poll3(message):
    poll_all(message, message.text, message.chat.id, poll3, 'опрос3')


def poll_all(message, text, id, f, txt):
    opti = wks.row_values(wks.find(txt).row)
    del opti[0:15]
    if opti.count(text) == 1:
        wks.update_cell(int(wks.find(txt).row + 1), int(opti.index(text) + 16),
                        int(wks.cell(wks.find(txt).row + 1, opti.index(text) + 16).value) + 1)
        bot.send_message(id, "Выберите опрос", reply_markup=poll_board)
        bot.register_next_step_handler(message, poll)
    elif message.text.lower() == 'назад':
        bot.send_message(id, "Выберите опрос", reply_markup=poll_board)
        bot.register_next_step_handler(message, poll)
    elif message.text.lower() != 'назад' and opti.count(text) != 1:
        bot.register_next_step_handler(message, f)


bot.polling()
