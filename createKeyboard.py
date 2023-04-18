import telebot
from loguru import logger
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
daysRU = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
daysSlovEn={'monday': 'Понедельник',
        'tuesday': 'Вторник',
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
        'saturday': 'Суббота',
        'sunday':'Воскресенье' }
def create_week_day_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    print('создаем клавиатуру недели')
    for day, dayRU in zip(days, daysRU):
        callBack = f'btnDay_{day}'
        title = dayRU 
        keyboard.add(telebot.types.InlineKeyboardButton(text = title,
            callback_data =callBack))
    return keyboard

def create_zanatia_for_user_day_keyboard(zanatias: list, callback: str): 
    keyboard = telebot.types.InlineKeyboardMarkup()
    for z in zanatias:
        callBack = callback.split('_')[1]
        title = str(z['title'], encoding='utf-8')
        zanatia_id = z['zanatie_id']
        keyboard.add(telebot.types.InlineKeyboardButton( text = title,
        callback_data =f'btnZan_{callBack}_{zanatia_id}'))
    return keyboard        

def create_zanatia_for_admin_day_keyboard(zanatiaWeek: list, callback: str): 
    keyboard = telebot.types.InlineKeyboardMarkup()
    for z in zanatiaWeek:
        callBack = callback.split('_')[1]
        name = str(z['name'], encoding='utf-8')
        zanatia_id = z['zanatie_id']
        user_id=z['user_id'] 
        keyboard.add(telebot.types.InlineKeyboardButton( text = title,
        callback_data =f'btnAdmin_{user_id}_{zanatia_id}'))
    return keyboard


def create_zanatia_for_user_keyboard(zanatias: list, ): 
    keyboard = telebot.types.InlineKeyboardMarkup()
    print('keyboard users zanatia ', zanatias)
    for z in zanatias:
        day = z['day'].decode()
        print('day',day)

        dayTitle = daysSlovEn[z['day'].decode()]
        print('dayTitle',dayTitle)
        title = str(z['title'], encoding='utf-8')
        print('title',title)
        zanatia_id = z['sanatie']
        keyboard.add(telebot.types.InlineKeyboardButton( text = title,
            callback_data =f'btnZan_{day}_{zanatia_id}'))
    return keyboard             

def create_menu_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Записаться на занятия')
    keyboard.row('Мой абонемент')
    keyboard.row('Мои занятия')
    
    return keyboard
