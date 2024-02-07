import json
import telebot
from telebot import types

import Path
import DBHandler


with open('token_api.json', 'r') as token_api:
    bot_token = json.load(token_api)
    
with open('text_message.json', 'r', encoding='utf-8') as text_message:
    bot_message = json.load(text_message)

bot = telebot.TeleBot(bot_token['token_api'])



@bot.message_handler(commands=['start'])
def startBot(message):
  markup = types.InlineKeyboardMarkup()
  first_message = f"<b>{message.from_user.first_name}</b>, <b>{bot_message['start_message']}</b>"
  button_menu_1 = types.InlineKeyboardButton(text = bot_message['menu_text_1'], callback_data='select_1')
  markup.row(button_menu_1)
  button_menu_2 = types.InlineKeyboardButton(text = bot_message['menu_text_2'], callback_data='select_2')
  markup.row(button_menu_2)
  button_menu_3 = types.InlineKeyboardButton(text = bot_message['menu_text_3'], callback_data='select_3')
  markup.row(button_menu_3)
  bot.send_message(message.chat.id, first_message, parse_mode='html', reply_markup=markup)
  
@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
  if function_call.message:
     markup = types.InlineKeyboardMarkup()
     menu_message = ""
     if function_call.data == "select_1":
        menu_message = f"{bot_message['bullying_info']}"
        markup.add(types.InlineKeyboardButton(text = bot_message['menu_text_1'], callback_data='select_1'),types.InlineKeyboardButton(text = bot_message['menu_text_3'], callback_data='select_3'))
        button_menu_1 = types.InlineKeyboardButton(text = bot_message['menu_text_1'])
        markup.add(button_menu_1)
        button_menu_2 = types.InlineKeyboardButton(text = bot_message['menu_text_3'])
        markup.add(button_menu_2)
        button_menu_3 = types.InlineKeyboardButton("Перейти на сайт", url="https://ru.wikipedia.org/wiki/%D0%A2%D1%80%D0%B0%D0%B2%D0%BB%D1%8F")
        markup.add(button_menu_3)
        bot.send_message(function_call.message.chat.id, menu_message, reply_markup=markup)
        bot.answer_callback_query(function_call.id)
     #git push -u origin mainif function_call.data == "select_2":

     if function_call.data == "select_3":
        menu_message = f"{bot_message['exit_message']}"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text = bot_message['exit_message_callback']))
        bot.send_message(function_call.message.chat.id, menu_message, reply_markup=markup)
        bot.answer_callback_query(function_call.id)

     
bot.infinity_polling()

