import workYDB
sql = workYDB.Ydb()

def check_user(user_id):
    """если пользователь есть в базе то возвращает True"""
    user = sql.select_query('users', ['*'], where=f'user_id = {user_id}')

    if len(user) == 0:
        return False
    else:
        return True

def get_paylod(user_id):
    print('payload')
    user = sql.select_query('users', ['*'], where=f'id = {user_id}')
    print('payload', user)
    return user[0]['payload']

def update_raspisanie(text: str):
    days = ['понедельник', 'вторник', 'среда',
            'четверг', 'пятница', 'суббота', 'воскресенье']
    daysSlov = {'Понедельник': 'monday',
                'Вторник': 'tuesday',
                'Среда': 'wednesday',
                'Четверг': 'thursday',
                'Пятница': 'friday',
                'Суббота': 'saturday',
                'Воскресенье': 'sunday'}

    text = text.strip().split('\n')
    dayName = ''
    dayDate = 0
    for string in text:
        if string == '':
            continue
        p = string.split(' ')
        if p[0].lower() in days:
            dayName = p[0]
            dayDate = p[1]
            continue
        time = p[0]
        
        event_id = create_event(day=dayDate, name=string, time=time)
        sql.insert_query(daysSlov[dayName], {
                         'zanatie_id': event_id, 'name': string})
   


