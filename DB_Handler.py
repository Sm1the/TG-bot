import sqlite3

def show_data_base_hfct_request():
   # Connect to the database
  try:
    conn = sqlite3.connect('safechild.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM hfct_request")
    db_list = cur.fetchall()
    out_list = ''
    for el in db_list:
        out_list += f'id: {el[0]}, user: {el[1]}, data_create: {el[2]}\n'
    print(out_list)
    cur.close()
    conn.close()
  except sqlite3.Error as ex:
    print(ex)  

def show_data_base_dim_request():
   # Connect to the database
  try:
    conn = sqlite3.connect('safechild.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM dim_request")
    db_list = cur.fetchall()
    out_list = ''
    for el in db_list:
        out_list += f'id: {el[0]}, user: {el[1]}, data_create: {el[2]}\n'
    print(out_list)
    cur.close()
    conn.close()
  except sqlite3.Error as ex:
    print(ex)  
    
def search_in_data_base():
    user_index = input("Enter date_create:")
   # Connect to the database
    try:
        conn = sqlite3.connect('safechild.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM dim_request WHERE attribute_id = '%s'" % (user_index))
        db_list = cur.fetchall()
        out_list = ''
        for el in db_list:
            out_list += f'attribute_id: {el[0]}, attribute_name: {el[1]}, attribute_value: {el[2]}\n'
        print(out_list)
        cur.close()
        conn.close()
    except sqlite3.Error as ex:
        print(ex)  
        


while True:
    print('''Выберите пункт меню :
1 - Show Data Base hfct_request ")
2 - Show Data Base dim_request ")
3 - Search in Data Base ")
4 - Выход
''')
    menu = input('Введите пункт меню >>> ')
    if menu == '1':
        show_data_base_hfct_request()
        
    elif menu == '2':
        show_data_base_dim_request()

    elif menu == '3':
        search_in_data_base()

    elif menu == '4':
        raise SystemExit

    else: print('Не существующий пункт') 