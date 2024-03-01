import json
import telebot
import datetime
import sqlite3
from telebot import types
from pathlib import Path

#Чтение ключа бота из json файла
with open('token_api.json', 'r') as token_api:
    bot_token = json.load(token_api)
#Чтение всего текста бота из json файла  
with open('text_message.json', 'r', encoding='utf-8') as text_message:
    bot_message = json.load(text_message)
#
with open('file_path.json', 'r', encoding='utf-8') as file_path:
    bot_file_path = json.load(file_path)
#Реализация соединения бота по ключу
bot = telebot.TeleBot(bot_token['token_api'])

#Метод очистки пользовательских кнопок
clear_unber_buttons = telebot.types.ReplyKeyboardRemove()
#Для хранения id пользователя
user_id = None
#Для хранения ответов от пользователя
user_name = None
user_city = None
user_school = None
user_bullying = None
user_violence = None
user_sexual_violence = None
bulllying_counter = None

current_time = datetime.datetime.now()

#Метод стартового меню и входа в общение с ботом
@bot.message_handler(commands=['start'])
def startBot(message):
  start_data_base()
  global user_id
  user_id = message.chat.id
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  first_message = f"<b>{message.from_user.first_name}</b><b>{bot_message['start_message']}</b>"
  button_menu_1 = types.KeyboardButton(text = bot_message['menu_text_1'])
  markup.row(button_menu_1)
  button_menu_2 = types.KeyboardButton(text = bot_message['menu_text_2'])
  markup.row(button_menu_2)
  button_menu_3 = types.KeyboardButton(text = bot_message['menu_text_3'])
  markup.row(button_menu_3)
  bot.send_message(message.chat.id, first_message, parse_mode='html', reply_markup=markup)
  bot.register_next_step_handler(message, on_click_menu)

#Обработчик первичного меню
def on_click_menu(message):
  if message.text == bot_message['menu_text_1']:
      bullying_info_bot(message)   
  if message.text == bot_message['menu_text_2']:
      user_data_accept(message)   
  if message.text == bot_message['menu_text_3']:
      exit_bot(message)

#Метод открытие пунка с информацией о буллинге      
def bullying_info_bot(message):
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      menu_message = f"{bot_message['bullying_info']}"
      markup.add(types.KeyboardButton(text = bot_message['menu_text_2']),types.KeyboardButton(text = bot_message['menu_text_3']))
      bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
      bot.register_next_step_handler(message, on_click_bullying_menu)

#Метод буллинг меню с переходом на создание обращения\закрытие диалога
def on_click_bullying_menu(message):
    if message.text == bot_message['menu_text_2']:
      user_data_accept(message)
    if message.text == bot_message['menu_text_3']:
      exit_bot(message)     

#Метод создания заявки     
def user_data_accept(message):
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      menu_message = f"{bot_message['copy_info']}"
      markup.add(types.KeyboardButton(bot_message['yes']),types.KeyboardButton(bot_message['no']))
      bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
      bot.register_next_step_handler(message, user_data_complite)

#Проверка на согласие пользователя на обработку данных
def user_data_complite(message):
    if message.text == bot_message['yes']:
      get_user_name(message)
    if message.text == bot_message['no']:
      cancellation_confirmation(message)

#Подтверждение закрытие диалога из-за отказа от обработки личных данных
def cancellation_confirmation(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_message = f"{bot_message['without_user_data_accept']}"
    markup.add(types.KeyboardButton(text = bot_message['sure_yes']),types.KeyboardButton(text = bot_message['no']))
    bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, complite_cancellation_confirmation)

#Обработчик отказа      
def complite_cancellation_confirmation(message):
    if message.text == bot_message['no']:
      get_user_name(message)
    if message.text == bot_message['sure_yes']:
      exit_bot(message)

#Метод закрытия диалога с ботом      
def exit_bot(message):
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      menu_message = f"{bot_message['exit_message']}"
      markup.add(types.KeyboardButton(text = bot_message['exit_message_callback']))
      bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)    

#Получение имени
def get_user_name(message):
      menu_message = f"{bot_message['user_name']}"
      bot.send_message(message.from_user.id, menu_message, parse_mode='html', reply_markup=clear_unber_buttons) 
      bot.register_next_step_handler(message, get_user_city)

#Получение города
def get_user_city(message):
    global user_name
    user_name = message.text.strip()
    menu_message = f"{bot_message['user_city']}"
    bot.send_message(message.from_user.id, menu_message, parse_mode='html', reply_markup=clear_unber_buttons) 
    bot.register_next_step_handler(message, get_user_school)


#Получение школы    
def get_user_school(message):
    global user_city
    user_city = message.text.strip()
    menu_message = f"{bot_message['user_school']}"
    bot.send_message(message.from_user.id, menu_message, parse_mode='html', reply_markup=clear_unber_buttons) 
    bot.register_next_step_handler(message, get_user_bullying)


#Получение буллинга  
def get_user_bullying(message):
    global user_school
    user_school = message.text.strip()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_message = f"{bot_message['user_bullying']}"
    markup.add(types.KeyboardButton(bot_message['yes']),types.KeyboardButton(bot_message['no']))
    bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, get_user_violence)

#Получение насилия   
def get_user_violence(message):
    global user_bullying
    if message.text == bot_message['yes']:
      user_bullying = bot_message['yes']
    if message.text == bot_message['no']:
      user_bullying = bot_message['no']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_message = f"{bot_message['user_violence']}"
    markup.add(types.KeyboardButton(bot_message['yes']),types.KeyboardButton(bot_message['no']))
    bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, get_user_sexual_violence)

#Получение сексуального насилия    
def get_user_sexual_violence(message):
    global user_violence
    if message.text == bot_message['yes']:
      user_violence = bot_message['yes']
    if message.text == bot_message['no']:
      user_violence = bot_message['no']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_message = f"{bot_message['user_sexual_violence']}"
    markup.add(types.KeyboardButton(bot_message['yes']),types.KeyboardButton(bot_message['no']))
    bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, get_user_bulllying_counter)

#Получение предложений от пользователя   
def get_user_bulllying_counter(message):
    global user_sexual_violence
    if message.text == bot_message['yes']:
      user_sexual_violence = bot_message['yes']
    if message.text == bot_message['no']:
      user_sexual_violence = bot_message['no']
    menu_message = f"{bot_message['bulllying_counter']}"
    bot.send_message(message.from_user.id, menu_message, parse_mode='html', reply_markup=clear_unber_buttons) 
    bot.register_next_step_handler(message, get_pull_user_info)

#Обработчик выбора загрузки файлов или отказ
def get_pull_user_info(message):
    global bulllying_counter
    if(message.text != bot_message['upload_file']):
      bulllying_counter = message.text.strip()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_message = f"{bot_message['pull_user_info']}"
    markup.add(types.KeyboardButton(bot_message['upload_file']), types.KeyboardButton(bot_message['without_file']))
    bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, select_user_send_file)

#Обработчик типа файлов от пользователя
def select_user_send_file(message):
    Path(bot_file_path['file_path'] + f'{message.chat.id}/').mkdir(parents=True, exist_ok=True)
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        file_size = int(message.photo[len(message.photo) - 1].file_size)
        if (file_size < 33554432):
          downloaded_file = bot.download_file(file_info.file_path)
          src = bot_file_path['file_path'] + f'{message.chat.id}/' + file_info.file_path.replace('photos/', '')
          with open(src, 'wb') as new_file:
              new_file.write(downloaded_file)
          bot.register_next_step_handler(message, user_correct_file)
        else:
            file_does_not_match(message) 
    elif message.content_type == 'video':
          file_info = bot.get_file(message.video.file_id)
          file_size = int(message.json['video']['file_size'])
          if (file_size < 268435456):
            downloaded_file = bot.download_file(file_info.file_path)
            src = bot_file_path['file_path'] + f'{message.chat.id}/' + file_info.file_path.replace('videos/', '')
            with open(src, 'wb') as new_file:
              new_file.write(downloaded_file)
            menu_message = f"{bot_message['wait_for_download']}"
            bot.send_message(message.chat.id, menu_message, parse_mode='html') 
            bot.register_next_step_handler(message, user_correct_file)
          else:
            file_does_not_match(message)  
    else:
          file_does_not_match(message)
           
    if message.text == bot_message['upload_file']:
      get_pull_user_info(message)  
      
    if message.text == bot_message['without_file']:
      close_user_request(message)

#Обработчик корректного файла
def user_correct_file(message):
  write_data_base()
  menu_message = f"{bot_message['correct_file']}"
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  markup.add(types.KeyboardButton(text = bot_message['exit_message_callback']))
  bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)

#Обработчик не корректного файла
def file_does_not_match(message):
      write_data_base()
      menu_message = f"{bot_message['file_does_not_match']}"
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      markup.add(types.KeyboardButton(text = bot_message['exit_message_callback']))
      bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup) 
  
#Обработчик закрытия диалога  
def close_user_request(message):
    write_data_base()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_message = f"{bot_message['close_user_request']}"
    markup.add(types.KeyboardButton(text = bot_message['exit_message_callback']))
    bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
 
#Создание БД и проверка на дубликат или повреждения
def start_data_base():
 # Connect to the database
  try:
    conn = sqlite3.connect('safechild.sql')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS hfct_request (id integer primary key AUTOINCREMENT, user varchar(50) not null, data_create varchar(50) not null)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS dim_request (attribute_id varchar(50), attribute_name varchar(50), attribute_value varchar(255), FOREIGN KEY (attribute_id) REFERENCES hfct_request (data_create))''')
    conn.commit()
    cur.close()
    conn.close()
  except sqlite3.Error as ex:
    print(ex)  

#Запись информации от пользователя в БД
def write_data_base():  
   # Connect to the database
  try:
    conn = sqlite3.connect('safechild.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO hfct_request (user, data_create) VALUES ('%s', '%s')" % (user_id, current_time))
    cur.execute("INSERT INTO dim_request (attribute_id, attribute_name, attribute_value) VALUES ('%s', '%s', '%s')" % (current_time, bot_message['user_name'], user_name)) 
    cur.execute("INSERT INTO dim_request (attribute_id, attribute_name, attribute_value) VALUES ('%s', '%s', '%s')" % (current_time, bot_message['user_city'], user_city)) 
    cur.execute("INSERT INTO dim_request (attribute_id, attribute_name, attribute_value) VALUES ('%s', '%s', '%s')" % (current_time, bot_message['user_school'], user_school)) 
    cur.execute("INSERT INTO dim_request (attribute_id, attribute_name, attribute_value) VALUES ('%s', '%s', '%s')" % (current_time, bot_message['user_bullying'], user_bullying)) 
    cur.execute("INSERT INTO dim_request (attribute_id, attribute_name, attribute_value) VALUES ('%s', '%s', '%s')" % (current_time, bot_message['user_violence'], user_violence)) 
    cur.execute("INSERT INTO dim_request (attribute_id, attribute_name, attribute_value) VALUES ('%s', '%s', '%s')" % (current_time, bot_message['user_sexual_violence'], user_sexual_violence)) 
    cur.execute("INSERT INTO dim_request (attribute_id, attribute_name, attribute_value) VALUES ('%s', '%s', '%s')" % (current_time, bot_message['bulllying_counter'], bulllying_counter))       
    conn.commit()
    cur.close()
    conn.close()
  except sqlite3.Error as ex:
    print(ex)  
  print(current_time,'new request from', user_id)

#Ограничитель на время обработки запросов от пользователей, в случае нагрузки изменить параметр interval на 2-5
try:
    print("Bot turn on :", current_time) 
    bot.polling(none_stop=True, interval=1)
except Exception as ex:
    print(ex)


