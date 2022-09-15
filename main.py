import psycopg2


def delete_tables(cur):
    '''Удаление таблиц.'''
    cur.execute("""
    DROP TABLE phone;
    DROP TABLE client;
    """)

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
        phone_number BIGINT UNIQUE NOT NULL CONSTRAINT phone_positive CHECK (phone_number > 0),
        CONSTRAINT phone_id PRIMARY KEY (client_id, phone_number)
    );
    """)
        
def add_new_client(cur, name, surname, email, phone_number=None):
    '''Добавление нового клиента.'''
    # v.1 - Просто создаём запись в отношении client.
    if phone_number == None: 
        cur.execute("""
        INSERT INTO client(name, surname, email) VALUES(%s, %s, %s);
        """, (name, surname, email))
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
        
def add_new_phone(cur, client_id, phone_number):
    '''Добавление номера телефона.'''
    cur.execute("""
    INSERT INTO phone(client_id, phone_number) VALUES(%s, %s);
    """, (client_id, phone_number))

def update_client_info(cur, client_id, name=None, surname=None, email=None, phone_number=None):
    '''Обновление информации о клиенте.'''
    if name != None: 
        cur.execute("""
        UPDATE client SET name=%s WHERE id=%s;
        """, (name, client_id))
    if surname != None: 
        cur.execute("""
        UPDATE client SET surname=%s WHERE id=%s;
        """, (surname, client_id))
    if email != None: 
        cur.execute("""
        UPDATE client SET email=%s WHERE id=%s;
        """, (email, client_id))
    if phone_number != None: 
        cur.execute("""
        UPDATE phone SET phone_number=%s WHERE client_id=%s;
        """, (phone_number, client_id))

def delete_phone_number(cur, client_id, phone_number):
    '''Удаление номера телефона.'''
    cur.execute("""
    DELETE FROM phone WHERE client_id=%s AND phone_number=%s;
    """, (client_id, phone_number))

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

def get_client_info(cur, name=None, surname=None, email=None, phone_number=None):
    '''Получить информацию о клиенте.'''
    if name != None: 
        cur.execute("""
        SELECT id, name, surname, email, phone_number FROM client AS c 
        LEFT JOIN phone AS p ON p.client_id = c.id
        WHERE name=%s;
        """, (name,))
        print(cur.fetchall())
    if surname != None: 
        cur.execute("""
        SELECT id, name, surname, email, phone_number FROM client AS c 
        LEFT JOIN phone AS p ON p.client_id = c.id
        WHERE surname=%s;
        """, (surname,))
        print(cur.fetchall())
    if email != None: 
        cur.execute("""
        SELECT id, name, surname, email, phone_number FROM client AS c 
        LEFT JOIN phone AS p ON p.client_id = c.id
        WHERE email=%s;
        """, (email,))
        print(cur.fetchone())
    if phone_number != None:
        cur.execute("""
        SELECT id, name, surname, email, phone_number FROM client AS c 
        LEFT JOIN phone AS p ON p.client_id = c.id
        WHERE phone_number=%s;
        """, (phone_number,))
        print(cur.fetchone())

if __name__ == "__main__":
    
    with psycopg2.connect(database='homework2', user='postgres', password='31288') as conn:
        with conn.cursor() as cur:
            #delete_tables(cur)
            #create_tables(cur)

            #add_new_client(cur, 'cl1name', 'cl1surname', 'cl1@m.com', phone_number=None)
            #add_new_client(cur, 'cl2name', 'cl2surname', 'cl2@m.com', 12345678901)
            #add_new_client(cur, 'cl3name', 'cl3surname', 'cl3@m.com', 12365478903)
            #add_new_client(cur, 'cl4name', 'cl4surname', 'cl4@m.com', phone_number=None)
            
            #add_new_phone(cur, 1, 79797977979)
            #add_new_phone(cur, 2, 74566544868)
            #add_new_phone(cur, 3, 15632478958)
            #add_new_phone(cur, 4, 98898989898)

            #update_client_info(cur, 1, name='cl1newname', surname=None, email=None, phone_number=None)
            #update_client_info(cur, 2, name=None, surname='cl2newsurname', email=None, phone_number=None)
            #update_client_info(cur, 3, name=None, surname=None, email='cl3@newm.com', phone_number=None)
            #update_client_info(cur, 4, name=None, surname=None, email=None, phone_number=11111110000)

            #delete_phone_number(cur, 2, 74566544868)
            #delete_client(cur, 4)

            #get_client_info(cur, name='cl2name', surname=None, email=None, phone_number=None)
            #get_client_info(cur, name=None, surname='cl3surname', email=None, phone_number=None)
            #get_client_info(cur, name=None, surname=None, email='cl2@m.com', phone_number=None)
            #get_client_info(cur, name=None, surname=None, email=None, phone_number=12365478903)
    
conn.close() 