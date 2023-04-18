import os
import ydb

driver = ydb.Driver(endpoint=os.getenv('YDB_ENDPOINT'),
                    database=os.getenv('YDB_DATABASE'),)
                    #credentials=ydb.AccessTokenCredentials(YDB_CREDINTALS_TOKEN))
# Wait for the driver to become active for requests.G
driver.wait(fail_fast=True, timeout=5)
# Create the session pool instance to manage YDB sessions.
pool = ydb.SessionPool(driver)


class Ydb:
    def insert_query(self, tableName: str, rows: dict):
        print('попали в инсерт')
        field_names = rows.keys()
        fields_format = ", ".join(field_names)
        my_list = list(rows.values())
    
        value = '('
        for i in my_list:
            try:
                value += f'{int(i)},'
            except Exception as e:
                print(e)
                if len(i.split('T')) == 2:
                    value += f"CAST('{i}' as datetime),"
                else:
                    value += f"'{i}',"
        value = value[:-1] + ')'
        # values_placeholder_format = ', '.join(my_list)
        query = f"INSERT INTO {tableName} ({fields_format}) VALUES {value}"
        print(query)

        def a(session):
            session.transaction(ydb.SerializableReadWrite()).execute(
                query,
                commit_tx=True,
            )
        return pool.retry_operation_sync(a)

    def update_query(self, tableName: str, rows: dict, where: str):
        # 'where id > 20 '
        field_names = rows.keys()
        fields_format = ", ".join(field_names)
        my_list = list(rows.values())
        sets = ''
        for key, value in rows.items():
            try:
                sets += f'{key} = {int(value)},'

            except Exception as e:
                print(e)
                sets += f"{key} = '{value}',"

        sets = sets[:-1]

        # values_placeholder_format = ', '.join(my_list)
        query = f'UPDATE {tableName} SET {sets} WHERE {where}'
        # query = f"INSERT INTO {tableName} ({fields_format}) " \
        print(query)

        def a(session):
            session.transaction(ydb.SerializableReadWrite()).execute(
                query,
                commit_tx=True,
            )
        return pool.retry_operation_sync(a)

    def delete_query(self, tableName: str, where: str):
        # 'where id > 20 '
        query = f'DELETE FROM {tableName} WHERE {where}'
        print(query)

        def a(session):
            session.transaction(ydb.SerializableReadWrite()).execute(
                query,
                commit_tx=True,
            )
        return pool.retry_operation_sync(a)

    def select_query(self, tableName: str, rows: list, where: str = None):
        field_names = rows
        fields_format = ", ".join(field_names)
        if where is None:
            query = f"SELECT {fields_format} FROM {tableName};"
        else:
            query = f"SELECT {fields_format} FROM {tableName} WHERE {where};"
        print(query)

        def a(session):
            return session.transaction().execute(
                query,
                commit_tx=True,
            )
        b = pool.retry_operation_sync(a)
        # string = b_string.decode('utf-8')
        # IndexError: list index out of range если нет данныйх
        rez = b[0].rows
        return rez

    def clear_all_days():
        days = ['monday', 'tuesday', 'wednesday',
                'thursday', 'friday', 'saturday', 'sunday']

        def a(session):
            session.transaction(ydb.SerializableReadWrite()).execute(
                query,
                commit_tx=True,
            )
        for day in days:
            query = f'DELETE FROM {day} WHERE zanatie_id != 1'
            print(query)
            pool.retry_operation_sync(a)
    
    def select_zanatia_for_user(self, user_id:int):
        # 'where id > 20 '
        query = f'SELECT * FROM users JOIN zanatia_week ON users.id = zanatia_week.user_id where id={user_id};'
        print(query)

        def a(session):
            return session.transaction().execute(
                query,
                commit_tx=True,
            )
        b = pool.retry_operation_sync(a)
        # string = b_string.decode('utf-8')
        # IndexError: list index out of range если нет данныйх
        print('b',b)
        rez = b[0].rows
        print('rez',rez)
        return rez


# пользователь по занятию


"""SELECT *
FROM users
JOIN zanatia_week ON users.id = zanatia_week.user_id;"""

# вся иформация из всех занятинй на неделю zanatia_weekЖ
"""SELECT *
FROM users
JOIN zanatia_week ON users.id = zanatia_week.user_id
JOIN friday ON zanatia_week.sanatie = friday.zanatie_id;
"""

def handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello World!',
    }
