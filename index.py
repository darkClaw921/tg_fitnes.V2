import os
import json
import workYDB
import messageQuery as que
from workTelegram import bot
import telebot
from datetime import datetime

sql = workYDB.Ydb()
def reg_user(message):
    sql.insert_query('users', {'id': message['user_id'],
     'name': message['user_first_name'],
     'last_name': message['user_last_name'],
     'payload': 'REG'})

def command_handler(message):
    comand = message['text']
    if comand == '/start':
        req_user(message) 
    pass

def btn_handler(message):

    pass


def handler(event, context):
    #message = que.get_message()
    #date = datetime.now().isoformat(timespec='seconds')+'Z'
    #a = sql.insert_query(tableName= 'zanatia_week', rows={'date':date,'sanatie': 567, 'user_id':53})
    #sql.select_zanatia_for_user(user_id= 400923372)
    p = event['messages'][0]['details']['message']['body']
    print(p)
    p=eval(p)
    message = telebot.types.Update.de_json(p['body'])

    bot.process_new_updates([message])
    #message = eval(p)
  
    return {
        'statusCode': 200,
        'body': 'Hello World!',
    }
