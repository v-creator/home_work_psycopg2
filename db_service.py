import psycopg2


def create_database(connection):
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


def load_id_client(connection, first_name, last_name):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT id FROM client WHERE first_name = %s and last_name = %s
                                """, (first_name, last_name))
        id_client = cursor.fetchone()
        return id_client


def append_phone(connection, first_name, last_name, phone):
    with connection.cursor() as cursor:
        id_client = load_id_client(connection, first_name, last_name)
        cursor.execute(f"""INSERT INTO client_phone (id_client,phone)
                            values (%s, %s)""", (id_client, phone))
        print('Номер добавлен клиенту', first_name, last_name)


def append_client(connection, first_name, last_name, email, phone=None):
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO client (first_name,last_name,email)
                            VALUES (%s, %s, %s)
                            """, (first_name, last_name, email))
        append_phone(connection, first_name, last_name, phone)
        print('Клиент добавлен')


# def update_client(connection, id=None, first_name=None, last_name=None, email=None, phone=None):
#     with connection.cursor() as cursor:
#         if id!=None:
#             id_client = id
#             print('1')
#         else:
#             id_client = load_id_client(connection, first_name, last_name)
#             print('2')
#         cursor.execute(f"""UPDATE client SET first_name = %s, last_name = %s
#                         where id = %s""", (first_name, last_name, id_client))
#         conn.commit()
#     print('Данные обновленны')

def delete_phone(connection, phone, id=None, first_name=None, last_name=None):
    if id != None:
        id_client = id
    else:
        id_client = load_id_client(connection, first_name, last_name)
    with connection.cursor() as cursor:
        cursor.execute("""DELETE FROM client_phone WHERE id_client = %s and phone = %s""", (id_client, phone))
    print('Номер удален ')


def delete_cleint(connection, id=None, first_name=None, last_name=None):
    if id != None:
        id_client = id
    else:
        id_client = load_id_client(connection, first_name, last_name)
    with connection.cursor() as cursor:
        cursor.execute(f"""DELETE FROM client_phone WHERE id_client = %s;
                            DELETE FROM client WHERE id = %s;""", (id_client, id_client))
    print('Клиент удален ')

def search_client(connection, first_name=None, last_name=None, email=None, phone=None):
    with connection.cursor() as cursor:
        if first_name!=None or last_name!=None or email!=None:
            cursor.execute(f"""SELECT * FROM client 
                                WHERE first_name = %s or last_name = %s or email = %s""",
                           (first_name,last_name,email))
            result = cursor.fetchall()
        else:
            id_client = cursor.execute(f"""SELECT id_client FROM client_phone 
                                WHERE phone = %s""", (phone,))
            print(id_client)
            cursor.execute(f"""SELECT * FROM client WHERE id = %s""",(id_client,))
            result = cursor.fetchall()

        return result



with psycopg2.connect(database = 'netology_db', user = 'postgres', password = 'postgres') as conn:
    # create_database(conn)
    # append_client(conn, 'Vlad', 'Ivanov', 'vlad@mail.ru', '89184957826')
    # append_client(conn, 'Serg', 'Petr', 'vlad@mail.ru', '89184955646')

    # append_phone(conn, 'Vlad', 'Ivanov', '89184957596')
    # update_client(conn, id='1', first_name='Vlad')
    # delete_phone(conn, id='1', phone='89184957596')
    # delete_cleint(conn, id=1)
    print(search_client(conn, phone='89184957826'))
conn.close()

