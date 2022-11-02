import psycopg2
from db_service import DBservice

service = DBservice()

def create_database(connection):
    """Функция, создающая структуру БД (таблицы)"""
    with connection.cursor() as cursor:
        cursor.execute(f"""create table client (
                            id serial primary key,
                            first_name varchar(40),
                            last_name varchar(40),
                            email varchar(40) not null
                        );
                        create table client_phone (
                            id serial primary key,
                            id_client integer not null,
                            phone varchar(40) UNIQUE,
	                        CONSTRAINT client_phone_fkey FOREIGN KEY (id_client) REFERENCES client(id)
                        );""")
        print('Созданы таблицы client и client_phone')


def append_phone(connection, first_name, last_name, phone):
    """Функция, позволяющая добавить телефон для существующего клиента"""
    with connection.cursor() as cursor:
        id_client = service.load_id_client(connection, first_name, last_name)
        cursor.execute(f"""INSERT INTO client_phone (id_client,phone)
                            values (%s, %s)""", (id_client, phone))
        print('Номер добавлен клиенту', first_name, last_name)


def append_client(connection, first_name, last_name, email, phone=None):
    """Функция, позволяющая добавить нового клиента"""
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO client (first_name,last_name,email)
                            VALUES (%s, %s, %s)
                            """, (first_name, last_name, email))
        append_phone(connection, first_name, last_name, phone)

        print('Клиент добавлен')


def update_client(connection, id=None, first_name=None, last_name=None, email=None, phone=None):
    """Функция, позволяющая изменить данные о клиенте"""
    id_client = service.checking_id(connection, id, first_name, last_name)
    columns = service.checking_variables(first_name, last_name, email).get('columns')
    values = service.checking_variables(first_name, last_name, email).get('values')
    with connection.cursor() as cursor:
        cursor.execute(f"""UPDATE client SET ({", ".join(columns)}) = ('{"', '".join(values)}')
                            where id = %s""", (id_client,))
        if phone != None:
            cursor.execute(f"""SELECT phone FROM client_phone WHERE id_client = %s""", (id_client,))
            list_number = cursor.fetchall()
            if len(list_number) > 0:
                update_number = input(f'{list_number}\nКакой номер хотите заменить?:')
                cursor.execute(f"""UPDATE client_phone SET phone = %s
                                            where id_client = %s and phone = %s""", (phone,id_client, update_number))
            else:
                cursor.execute(f"""INSERT INTO client_phone (id_client, phone) VALUES (%s, %s)""", (id_client, phone))
                print('Номер добавлен в базу')
        conn.commit()
    print('Данные обновленны')


def delete_phone(connection, phone, id=None, first_name=None, last_name=None):
    """Функция, позволяющая удалить телефон для существующего клиента"""
    id_client = service.checking_id(connection, id, first_name, last_name)
    with connection.cursor() as cursor:
        cursor.execute("""DELETE FROM client_phone WHERE id_client = %s and phone = %s""", (id_client, phone))
    print('Номер удален ')


def delete_cleint(connection, id=None, first_name=None, last_name=None):
    """Функция, позволяющая удалить существующего клиента"""
    id_client = service.checking_id(connection, id, first_name, last_name)
    with connection.cursor() as cursor:
        cursor.execute(f"""DELETE FROM client_phone WHERE id_client = %s;
                            DELETE FROM client WHERE id = %s;""", (id_client, id_client))
    print('Клиент удален ')


def search_client(connection, first_name=None, last_name=None, email=None, phone=None):
    with connection.cursor() as cursor:
        if phone != None:
            cursor.execute(f"""SELECT id_client FROM client_phone WHERE phone = %s""", (phone,))
            id_client = cursor.fetchall()
            if len(id_client) != 0:
                cursor.execute(f"""SELECT id, first_name, last_name, email 
                                    FROM client
                                    WHERE id = %s or first_name = %s or last_name = %s or email = %s""",
                               (id_client[0][0], first_name, last_name, email))
                result = cursor.fetchall()
            else:
                cursor.execute(f"""SELECT id, first_name, last_name, email 
                                    FROM client
                                    WHERE first_name = %s or last_name = %s or email = %s""", (first_name, last_name, email))
                result = cursor.fetchall()
        else:
            cursor.execute(f"""SELECT id, first_name, last_name, email 
                                FROM client
                                WHERE first_name = %s or last_name = %s or email = %s""", (first_name, last_name, email))
            result = cursor.fetchall()
        print(result)


with psycopg2.connect(database = 'netology_db', user = 'postgres', password = 'postgres') as conn:
    # create_database(conn)
    append_client(conn, 'Vlad', 'Ivanov', 'vlad@mail.ru', '89184957826')
    # append_client(conn, 'Serg', 'Petr', 'vlad@mail.ru', '89184955646')

    # append_phone(conn, 'Vlad', 'Ivanov', '89184957596')
    # update_client(conn, id='4', first_name='Mihans', email='mihas@mail.ru', phone='89156975647')
    # delete_phone(conn, id='1', phone='89184957596')
    # delete_cleint(conn, id=1)
    # print(search_client(conn, phone='89184957826'))
    # upgrade(first_name='Vladislav',email='89184957596')
    # search_client(conn, first_name='Mihans')
conn.close()

