
class DBservice:
    def checking_variables(self, first_name=None, last_name=None, email=None):
        """Вспомагательная функция, позволяющая сгенерировать структуру для обновления данных пользователя"""
        columns = []
        values = []
        result = {}
        if first_name != None:
            columns.append('first_name')
            values.append(first_name)
        if last_name != None:
            columns.append('last_name')
            values.append(last_name)
        if email != None:
            columns.append('email')
            values.append(email)
        result['columns'] = columns
        result['values'] = values
        return result


    def load_id_client(self, connection, first_name, last_name):
        """Вспомагательная функция, позволяющая определить id существующего клиента"""
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT id FROM client WHERE first_name = %s and last_name = %s
                                    """, (first_name, last_name))
            id_client = cursor.fetchone()
            return id_client


    def checking_id(self, connection, id=None, first_name=None, last_name=None):
        """Вспомагательная функция, позволяющая определить id пользователя"""
        if id != None:
            id_client = id
        else:
            id_client = self.load_id_client(self, connection, first_name, last_name)
        return id_client