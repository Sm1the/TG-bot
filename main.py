import json
import telebot
from telebot import types

import Path
import DBHandler

#Show DB List
#Close bot
#Restart bot



#Чтение ключа бота из json файла
with open('token_api.json', 'r') as token_api:
    bot_token = json.load(token_api)
#Чтение всего текста бота из json файла  
with open('text_message.json', 'r', encoding='utf-8') as text_message:
    bot_message = json.load(text_message)
#Реализация соединения бота по ключу
bot = telebot.TeleBot(bot_token['token_api'])


#Метод стартового меню и входа в общение с ботом
@bot.message_handler(commands=['start'])
def startBot(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  first_message = f"<b>{message.from_user.first_name}</b>, <b>{bot_message['start_message']}</b>"
  button_menu_1 = types.KeyboardButton(text = bot_message['menu_text_1'])
  markup.row(button_menu_1)
  button_menu_2 = types.KeyboardButton(text = bot_message['menu_text_2'])
  markup.row(button_menu_2)
  button_menu_3 = types.KeyboardButton(text = bot_message['menu_text_3'])
  markup.row(button_menu_3)
  bot.send_message(message.chat.id, first_message, parse_mode='html', reply_markup=markup)
  bot.register_next_step_handler(message, on_click_menu)
  

def on_click_menu(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  menu_message = ""
  if message.text == bot_message['menu_text_1']:
    menu_message = f"{bot_message['bullying_info']}"
    markup.add(types.KeyboardButton(text = bot_message['menu_text_2']),types.KeyboardButton(text = bot_message['menu_text_3']))
    bot.register_next_step_handler(message, on_click_second_menu)
    
  if message.text == bot_message['menu_text_2']:
      menu_message = f"{bot_message['copy_info']}"
      markup.add(types.KeyboardButton(text = 'Да'),types.KeyboardButton(text = 'Нет'))
      bot.register_next_step_handler(message, create_application)
    
  if message.text == bot_message['menu_text_3']:
      menu_message = f"{bot_message['exit_message']}"
      markup.add(types.KeyboardButton(text = bot_message['exit_message_callback']))

    
  bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
  

def on_click_second_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_message = ""
    if message.text == bot_message['menu_text_2']:
      menu_message = f"{bot_message['copy_info']}"
      markup.add(types.KeyboardButton(text = 'Да'),types.KeyboardButton(text = 'Нет'))
      bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
      bot.register_next_step_handler(message, create_application)
    if message.text == bot_message['menu_text_3']:
      exit_bot(message)


#Метод закрытия диалога с ботом      
def exit_bot(message):
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      menu_message = f"{bot_message['exit_message']}"
      markup.add(types.KeyboardButton(text = bot_message['exit_message_callback']))
      bot.send_message(message.chat.id, menu_message, parse_mode='html', reply_markup=markup)
    

    
     
bot.polling(non_stop=True)

