import sqlite3

def create_database():
    conn = sqlite3.connect('meet21.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS meet (
                      id INTEGER PRIMARY KEY,
                      description TEXT NOT NULL,
                      date TEXT NOT NULL,
                      site TEXT NOT NULL,
                      price TEXT NOT NULL,
                      place TEXT NOT NULL)''')
    conn.commit()
    desc = """Сходка пройдёт в очень крутом баре под названием Freedom!
Мы имеем удобное расположение, хороший дизайн и неплохие цены. 
Меню небольшое, но имеет все необходимое - и поесть и выпить. Кстати, у них неплохие крафтовые настойки, рекомендую
Мы выкупили второй этаж, так что нас бесопокить не будут, зона полностью приватная. Плюс сделают перестановку чтобы смогло разместится до 35 человек сидячими."""
    date = "09.03 18:00-02:00"
    place = "Большая Новодмитровская улица, 36 ст6"
    site = "freedombar.ru"
    price = "300p"
    cursor.execute('''INSERT INTO meet (description, date, site, price, place)
                      VALUES (?, ?, ?, ?, ?)''', (desc, date, site, price, place))

    conn.commit()
    conn.close()

def create_orders_table():
    conn = sqlite3.connect('meet21.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                      id INTEGER PRIMARY KEY,
                      username TEXT NOT NULL,
                      "order" TEXT NOT NULL,
                      price REAL NOT NULL)''')

    conn.commit()
    conn.close()

def get_meet_info():
    conn = sqlite3.connect('meet21.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT description, date, site, price, place FROM meet''')
    rows = cursor.fetchall()
    conn.close()
    desc, date, site, price, place = rows[0] 
    return desc, date, site, price, place	

def insert_order(username, order, price):
    conn = sqlite3.connect('meet21.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO orders (username, "order", price)
                      VALUES (?, ?, ?)''', (username, order, price))

    conn.commit()
    conn.close()

def get_orders_by_username(username):
    conn = sqlite3.connect('meet21.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT "order", price FROM orders
                      WHERE username = ?''', (username,))

    rows = cursor.fetchall()

    conn.close()

    orders = []
    for row in rows:
        order, price = row
        orders.append({
            'order': order,
            'price': price
        })

    return orders

if __name__ == '__main__':
    create_database()
    create_orders_table()
    desc, date, site, price, place =  get_meet_info()
    print(desc, date, site, price, place)
