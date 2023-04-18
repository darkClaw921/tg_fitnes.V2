from bitrix24 import Bitrix24
from pprint import pprint
import datetime
import os
bit = Bitrix24(os.getenv('WEBHOOK'))

#UF_CRM_CAL_EVENT элементы CRM контакт C_270 сделка D_270
def create_event(day: int, name:str, time:str):
    """
    [day]:int - (1 - 31)
    [name]:str - Прес и спина Люба
    [time]:str - 18:00
    """
    #a = bit.callMethod('calendar.event.get', type='company_calendar') #ownerId='1')
    endTime = time.split(':')
    endTime = f'{int(endTime[0])+1}:{endTime[1]}'
    date = datetime.date.today() # datetime.date(2017, 4, 5)
    a = bit.callMethod('calendar.event.add', TYPE='company_calendar', 
            to = f'{date.year}-{date.month}-{day} {endTime}',
            ownerId=' ',#10
            FROM=f'{date.year}-{date.month}-{day} {time}',
            section=1,#8
            name=f'{name}',
            location='Зал 1',
            is_meeting='Y',
            )
    return a
        


def get_event(ID:int):
    """
    Возвращает список имен и id пользователей записанных в календаре >
    """

    #date = datetime.date.today() # datetime.date(2017, 4, 5)
    #endTime = time.split(':')
    #endTime = f'{int(endTime[0])+1}:{endTime[1]}'
    sql = SqlLite('Users.db','')
    #print(ID)
    b = bit.callMethod('calendar.event.getbyid', ID=ID) 
    #print(b)

    try:
        users = b['UF_CRM_CAL_EVENT']
    except:
        users = None

    if users == None or users==False:
        return [],[]
    tempList=[]
    tempListId=[] 
    for user in users:
        user=user.split('_')[1]
        #print('for', user)
        b = bit.callMethod('crm.contact.get', ID= user) 
        #pprint(b)
        phone = b['PHONE'][0]['VALUE']
        firstName = b['NAME']
        lastName = b['LAST_NAME']
        name =f'{firstName} {lastName}'
        tempList.append(name)
        tempListId.append(user)
        try:
            sql.send(f"""insert into users (user_id, phone, user_name) values ({user}, {phone}, "{name}") """)
        except:
            print()
    return tempList, tempListId
