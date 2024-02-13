import json
import telebot
from telebot import types


#Show DB List
#Close bot
#Restart bot



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

#
clear_unber_buttons = telebot.types.ReplyKeyboardRemove()

#
user_name = ""
user_city = ""
user_school = ""
user_bullying = ""
user_violence = ""
user_sexual_violence = ""
bulllying_counter = ""



#Метод стартового меню и входа в общение с ботом
@bot.message_handler(commands=['start'])
def startBot(message):
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

#
def user_data_complite(message):
    if message.text == bot_message['yes']:
      get_user_name(message)
    if message.text == bot_message['no']:
      cancellation_confirmation(message)

#
def cancellation_confirmation(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_message = f"{bot_message['without_user_data_accept']}"
    markup.add(types.KeyboardButton(text = bot_message['sure_yes']),types.KeyboardButton(text = bot_message['no']))
    bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, complite_cancellation_confirmation)

#      
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
    
#
def get_user_name(message):
      menu_message = f"{bot_message['user_name']}"
      bot.send_message(message.from_user.id, menu_message, parse_mode='html', reply_markup=clear_unber_buttons) 
      bot.register_next_step_handler(message, get_user_city)

def get_user_city(message):
    user_name = message.text
    menu_message = f"{bot_message['user_city']}"
    bot.send_message(message.from_user.id, menu_message, parse_mode='html', reply_markup=clear_unber_buttons) 
    bot.register_next_step_handler(message, get_user_school)
    print(user_name)
    
def get_user_school(message):
    user_city = message.text
    menu_message = f"{bot_message['user_school']}"
    bot.send_message(message.from_user.id, menu_message, parse_mode='html', reply_markup=clear_unber_buttons) 
    bot.register_next_step_handler(message, get_user_bullying)
    print(user_city)
    
def get_user_bullying(message):
    user_school = message.text
    print(user_school)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_message = f"{bot_message['user_bullying']}"
    markup.add(types.KeyboardButton(bot_message['yes']),types.KeyboardButton(bot_message['no']))
    bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, get_user_violence)
   
def get_user_violence(message):
    if message.text == bot_message['yes']:
      user_bullying = bot_message['yes']
      print(user_bullying)
    if message.text == bot_message['no']:
      user_bullying = bot_message['no']
      print(user_bullying)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_message = f"{bot_message['user_violence']}"
    markup.add(types.KeyboardButton(bot_message['yes']),types.KeyboardButton(bot_message['no']))
    bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, get_user_sexual_violence)
      
def get_user_sexual_violence(message):
    if message.text == bot_message['yes']:
      user_violence = bot_message['yes']
      print(user_violence)
    if message.text == bot_message['no']:
      user_violence = bot_message['no']
      print(user_violence)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_message = f"{bot_message['user_sexual_violence']}"
    markup.add(types.KeyboardButton(bot_message['yes']),types.KeyboardButton(bot_message['no']))
    bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, get_user_bulllying_counter)
    
def get_user_bulllying_counter(message):
    if message.text == bot_message['yes']:
      user_sexual_violence = bot_message['yes']
      print(user_sexual_violence)
    if message.text == bot_message['no']:
      user_sexual_violence = bot_message['no']
      print(user_sexual_violence)
    menu_message = f"{bot_message['bulllying_counter']}"
    bot.send_message(message.from_user.id, menu_message, parse_mode='html', reply_markup=clear_unber_buttons) 
    bot.register_next_step_handler(message, get_pull_user_info)

def get_pull_user_info(message):
    bulllying_counter = message.text
    print(bulllying_counter)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_message = f"{bot_message['pull_user_info']}"
    markup.add(types.KeyboardButton(bot_message['upload_file']),types.KeyboardButton(bot_message['without_file']))
    bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, select_user_send_file)

def select_user_send_file(message):
    if message.text == bot_message['upload_file']:
      handle_docs_photo(message)
    if message.text == bot_message['without_file']:
      close_user_request(message)


@bot.message_handler(content_types=['photo', 'video'])
def handle_docs_photo(message):

    try:


        file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src='C:/Users/apxah/Desktop/1/TG-bot/files/'+file_info.file_path
        with open(src, 'wb') as new_file:
           new_file.write(downloaded_file)
        bot.reply_to(message,"Фото добавлено") 

    except Exception as e:
        bot.reply_to(message,e )
    
def close_user_request(message):
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      menu_message = f"{bot_message['close_user_request']}"
      markup.add(types.KeyboardButton(text = bot_message['exit_message_callback']))
      bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)

bot.polling(non_stop=True)

