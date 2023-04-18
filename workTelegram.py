import os
import random
import telebot
import workYDB
from createKeyboard import *
from calendar import *
from datetime import datetime
from helper import *

bot = telebot.TeleBot(os.getenv('TELEBOT_TOKEN'))
sql = workYDB.Ydb()
# инициализация бота и диспетчера
#dp = Dispatcher(bot)

@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    bot.send_message(message.chat.id,
                     'Hi, there! I am hosted by Yandex.Cloud Functions.\n'
                     'For more info click [here](https://github.com/otter18/serverless-tg-bot)',
                     parse_mode='markdown')

#@bot.callback_query_handler(startswitch('')
#@bot.callback_query_handler(Text(startswith='btn') or Text(startswith='btni_'))


#if call.data == 'test':
#    bot.send_message(call.chat.id, 'Hello')
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call): 
    btn = call.data.split('_')[0]
    print('callback: ',btn)
    if btn == 'btn':
        keyboard = create_week_day_keyboard()
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"это btn",reply_markup=keyboard )
    
    if btn == 'btnDay':
        print('создаем расписание')
        dayWeek = call.data.split('_')[1]
        result = sql.select_query(dayWeek, ['*'])
        print(result)
        keyboard = create_zanatia_for_user_day_keyboard(zanatias=result, 
            callback=call.data)
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 
            f"Расписание на {dayWeek}",
            reply_markup=keyboard )
    if btn == 'btnZan':
        splitCall=call.data.split('_')
        print('call',call)
        sql.delete_query('zanatia_week',
            where = f'user_id ={call.message.chat.id} and sanatie={splitCall[2]}')

        result = sql.select_query(splitCall[1],
          ['title'],
          where=f'zanatie_id = {splitCall[2]}')
        title = str(result[0]['title'], encoding='utf-8')

        date = datetime.now().isoformat(timespec='seconds')+'Z'
        sql.insert_query(tableName= 'zanatia_week', 
            rows={'date':date,
            'day': splitCall[1],
            'sanatie': splitCall[2],
            'title': title, 
            'user_id':call.message.chat.id})
        #sql.insert_query(tableName= 'zanatia_week', rows={'sanatie': splitCall[2], 'user_id':call.message.user.id})
        keyboard = create_menu_keyboard()
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 
            f"Вы записаны на {title}",
            reply_markup=keyboard )

        """
        keyboard = create_zanatia_for_user_day_keyboard()
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"это btn",reply_markup=keyboard )
        """
    #print('отпровляем кнопки бэк')
    #zanatie = call.data
    #print(call)
    #bot.answer_callback_query(
    #        call.id,
    #        text=f'вы записаны на {zanatie} ',)
    #bot.send_message(call.message.chat.id, f"это {zanatie}",)
    
@bot.message_handler(commands=['update'])
def send_button(message):
    print('обновляем расписание')
    #keyboard=create_menu_keyboard()
    bot.send_message(message.chat.id, 
        "Пришлите расписание")
    sql.update_query('users', {'payload':'UPDATE'},where = f'user_id = {message.chat.id}')


@bot.message_handler(commands=['button'])
def send_button(message):
    print('отпровляем кнопки')
    keyboard=create_menu_keyboard()
    bot.send_message(message.chat.id, 
        "На какой день хотите записаться?", 
        reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def any_message(message):
    print('это сообщение', message)
    text = message.text.lower()
    userID= message.chat.id
    payload = get_paylod(userID)
    if payload == 'UPDATE':
        bot.send_message(message.chat.id, f"Расписание обновляеться, это может занять какое-то время", )    
        update_raspisanie(message.text)
        
    if text == 'записаться на занятия':
        keyboard = create_week_day_keyboard()
        #bot.answer_callback_query(message.chat.id)
        bot.send_message(message.chat.id, f"Выберите день недели:",reply_markup=keyboard )    
    
    elif text == 'мои занятия':
        zanatias = sql.select_zanatia_for_user(userID)
        keyboard = create_zanatia_for_user_keyboard(zanatias)
        bot.send_message(message.chat.id, f"Ваши занятия:",reply_markup=keyboard )


    else:
        bot.send_message(message.chat.id, f"Попробуйте еще раз",)
        result = sql.select_query('friday', ['*'])
        for r in result:
            title = str(r['title'], encoding='utf-8')
            time = title.split(' ')[0]
            create_event(day=19, name=title, time=time)
