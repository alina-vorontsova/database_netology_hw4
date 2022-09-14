import psycopg2


def create_tables(cur):
    '''Создание отдельных таблиц для клиентов и для номеров клиентов.'''
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY,
        name VARCHAR(40) NOT NULL,
        surname VARCHAR (80) NOT NULL,
        email VARCHAR(80) UNIQUE NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phone(
        client_id INTEGER REFERENCES client(id),
        phone_number INTEGER UNIQUE NOT NULL CONSTRAINT phone_positive CHECK (phone_number > 0),
        CONSTRAINT phone_id PRIMARY KEY (client_id, phone_number)
    );
    """)
    conn.commit()
    print('Созданы таблицы client и phone.')
        
def add_new_client(cur, name, surname, email, phone_number=None):
    '''Добавление нового клиента.'''
    # v.1 - Просто создаём запись в отношении client.
    if phone_number == None: 
        cur.execute("""
        INSERT INTO client(name, surname, email) VALUES(%s, %s, %s);
        """, (name, surname, email))
        conn.commit()
        print('Добавлена запись о новом клиенте.', commands, sep='\n')
    # v.2 - Создаём запись в отношении client, "вынимаем" оттуда id клиента и по нему добавляем номер в отношение phone.
    elif phone_number != None: 
        cur.execute("""
        INSERT INTO client(name, surname, email) VALUES(%s, %s, %s);
        """, (name, surname, email))
        cur.execute("""
        SELECT id FROM client WHERE email=%s;
        """, (email,))
        clients_id = cur.fetchone()[0]
        cur.execute("""
        INSERT INTO phone(client_id, phone_number) VALUES(%s, %s);
        """, (clients_id, phone_number))            
        conn.commit()
        print('Добавлена запись о новом клиенте.', commands, sep='\n')
        
def add_new_phone(cur, client_id, phone_number):
    '''Добавление номера телефона.'''
    cur.execute("""
    INSERT INTO phone(client_id, phone_number) VALUES(%s, %s);
    """, (client_id, phone_number))
    conn.commit()
    print('Добавлен номер телефона.', commands, sep='\n')

def update_client_info(cur):
    '''Обновление информации о клиенте.'''
    client_id = int(input('Введите id клиента: '))
    print('Для обновления информации о клиенте введите номер команды: ', '1. Изменить имя', '2. Изменить фамилию', '3. Изменить e-mail', '4. Изменить номер телефона', sep='\n')
    while True: 
        command = int(input())
        if command == 1:
            cur.execute("""
            UPDATE client SET name=%s WHERE id=%s;
            """, (input('Введите новое имя: '), client_id))
            conn.commit()
            print('Обновлено имя.', commands, sep='\n')
            break 
        elif command == 2:
            cur.execute("""
            UPDATE client SET surname=%s WHERE id=%s;
            """, (input('Введите новую фамилию: '), client_id))
            conn.commit()
            print('Обновлена фамилия.', commands, sep='\n')
            break 
        elif command == 3:
            cur.execute("""
            UPDATE client SET email=%s WHERE id=%s;
            """, (input('Введите новый e-mail: '), client_id))
            conn.commit()
            print('Обновлён e-mail.', commands, sep='\n')
            break 
        elif command == 4:
            cur.execute("""
            UPDATE phone SET phone_number=%s WHERE client_id=%s AND phone_number=%s;
            """, (int(input('Введите новый номер телефона: ')), client_id, int(input('Введите старый номер телефона, подлежащий обновлению: '))))
            conn.commit()
            print('Обновлён номер телефона.', commands, sep='\n')
            break 
        else:
            print('Ошибка. Команда не найдена. Введите другую команду:', commands)
            break 

def delete_phone_number(cur, client_id, phone_number):
    '''Удаление номера телефона.'''
    cur.execute("""
    DELETE FROM phone WHERE client_id=%s AND phone_number=%s;
    """, (client_id, phone_number))
    conn.commit()
    print('Удалён номер телефона.', commands, sep='\n')

def delete_client(cur, client_id):
    '''Удаление клиента.'''
    # Сначала удаляется запись из отношения phone.
    cur.execute("""
    DELETE FROM phone WHERE client_id=%s; 
    """, (client_id,))
    # Затем удаляется запись из отношения client. 
    cur.execute("""
    DELETE FROM client WHERE id=%s;
    """, (client_id,))
    conn.commit()
    print('Удалён клиент.', commands, sep='\n')

def get_client_info(cur):
    '''Получить информацию о клиенте.'''
    print('Введите номер команды:', '1. Найти клиента по id', '2. Найти клиента по имени', '3. Найти клиента по фамилии', '4. Найти клиента по e-mail', '5. Найти клиента по номеру телефона', sep='\n')
    while True: 
        command = int(input())
        if command == 1:
            cur.execute("""
            SELECT id, name, surname, email, phone_number FROM client AS c 
            LEFT JOIN phone AS p ON p.client_id = c.id
            WHERE id=%s;
            """, (int(input('Введите id клиента: ')),))
            print(cur.fetchone())
            print(commands, sep='\n')
            break 
        if command == 2:
            cur.execute("""
            SELECT id, name, surname, email, phone_number FROM client AS c 
            LEFT JOIN phone AS p ON p.client_id = c.id
            WHERE name=%s;
            """, (input('Введите имя клиента: '),))
            print(cur.fetchall())
            print(commands, sep='\n')
            break 
        elif command == 3:
            cur.execute("""
            SELECT id, name, surname, email, phone_number FROM client AS c 
            LEFT JOIN phone AS p ON p.client_id = c.id
            WHERE surname=%s;
            """, (input('Введите фамилию клиента: '),))
            print(cur.fetchall())
            print(commands, sep='\n')
            break 
        elif command == 4:
            cur.execute("""
            SELECT id, name, surname, email, phone_number FROM client AS c 
            LEFT JOIN phone AS p ON p.client_id = c.id
            WHERE email=%s;
            """, (input('Введите e-mail клиента: '),))
            print(cur.fetchone())
            print(commands, sep='\n')
            break 
        elif command == 5:
            cur.execute("""
            SELECT id, name, surname, email, phone_number FROM client AS c 
            LEFT JOIN phone AS p ON p.client_id = c.id
            WHERE phone_number=%s;
            """, (int(input('Введите телефон клиента: ')),))
            print(cur.fetchone())
            print(commands, sep='\n')
            break 
        else:
            print('Ошибка. Команда не найдена. Введите другую команду:', commands, sep='\n')
            break

with psycopg2.connect(database='homework2', user='postgres', password='postgres') as conn:
    with conn.cursor() as cur:
        create_tables(cur)
        commands = 'Выберите номер команды:\n1. Добавить нового клиента\n2. Добавить номер клиента\n3. Обновить информацию о клиенте\n4. Удалить номер телефона\n5. Удалить клиента\n6. Получить информацию о клиенте\n7. Выход'
        print(commands)
        while True: 
            command = int(input())
            if command == 1:
                name, surname, email = input('Введите имя клиента: '), input('Введите фамилию клиента: '), input('Введите e-mail клиента: ')
                answer = int(input('Нажмите "1", чтобы сразу добавить номер телефона клиента. Нажмите "0", чтобы пока пропустить этот шаг.'))
                if answer == 1: 
                    phone_number = int(input('Введите номер телефона клиента: '))
                    add_new_client(cur, name, surname, email, phone_number)
                elif answer == 0:
                    add_new_client(cur, name, surname, email)
            elif command == 2:
                client_id, phone_number = int(input('Введите id клиента: ')), int(input('Введите номер телефона: '))
                add_new_phone(cur, client_id, phone_number)
            elif command == 3:
                update_client_info(cur)
            elif command == 4:
                client_id, phone_number = input('Введите id клиента: '), int(input('Введите номер телефона: '))
                delete_phone_number(cur, client_id, phone_number)
            elif command == 5:
                client_id = int(input('Введите id клиента: '))
                delete_client(cur, client_id)
            elif command == 6:
                get_client_info(cur)
            elif command == 7:
                break 
            else:
                print('Ошибка. Команда не найдена. Введите другую команду.')