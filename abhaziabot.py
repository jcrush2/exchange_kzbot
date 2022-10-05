#!usr/bin/python3
import datetime
import hashlib
import string
import os
from flask import Flask, request
import peewee as pw
import telebot

import config

TELEGRAM_API = os.environ["telegram_token"]
bot = telebot.TeleBot(TELEGRAM_API)
    
@bot.message_handler(commands=["start"])
def start(msg):
	bot.send_message(msg.chat.id, "Добро пожаловать в проверенный сервис обмена рублей на тенге",parse_mode="HTML")
	
	main(msg)
	
		
@bot.message_handler(commands=["main"])
def main(msg):
	keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	khvtrip = telebot.types.KeyboardButton(text="🇰🇿 Обмен RUB->KZ")
	servise = telebot.types.KeyboardButton(text="ℹ️ Помощь")

	keyboard.add( khvtrip, servise)
	bot.send_message(msg.chat.id, "Проверенный обменник в Казахстане ⬇️", reply_markup=keyboard)

	
	
@bot.callback_query_handler(func=lambda call: True)
def longname(call):
	a = datetime.datetime.today()

	if call.data == "exchange":
		sent =bot.send_message(call.message.chat.id, text="Введите номер карты Каспи банка ⬇")
		bot.register_next_step_handler(sent, love_foto)
		return
	if call.data == "Отмена":
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Отменено.')
def love_foto(msg):
	bot.forward_message(-886511861, msg.chat.id, msg.message_id)
	bot.send_message(-886511861, f"№ карты от: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.first_name}</a> id: {msg.from_user.id}", parse_mode="HTML")
	bot.send_message(msg.chat.id, f"Введите сумму в рублях ⬇", parse_mode="HTML")

		
		

def helps(msg):
	bot.send_message(msg.chat.id, f"Обмен производиться в ручном режиме.\n\nЧасы работы с 7:00 по 22:00 по мск.\n\nВремя обработки заявки 3-5 мин.\n\nПеревод отправлять без комментария! Заявки с комментарием обрабатываться не будут!\n\nМинимальная сумма обмена 1000 руб️.", parse_mode="HTML")

@bot.message_handler(commands=["exchange"])
def exchange(msg):
	chanel ="Обмен производиться в ручном режиме.\n\nЧасы работы с 7:00 по 22:00 по мск.\n\nВремя обработки заявки 3-5 мин.\n\nПеревод отправлять без комментария! Заявки с комментарием обрабатываться не будут!\n\nМинимальная сумма обмена 1000 руб️."
	markup = telebot.types.InlineKeyboardMarkup()
	button0 = telebot.types.InlineKeyboardButton(text="Обменять RUB->KZ", callback_data="exchange")

	markup.add(button0)
	
	sent =bot.send_message(chat_id=msg.chat.id, text=f"{chanel}️", reply_markup=markup)
	    
@bot.message_handler(content_types=['text', 'document', 'photo', 'audio', 'video','voice'])
def all_messages(msg):
	TO_CHAT_ID= -886511861
		
	if msg.text == "ℹ️ Помощь":
		helps(msg)
		return
		
	if msg.text == "🇰🇿 Обмен RUB->KZ":
		exchange(msg)
		return


	if msg.chat.id == TO_CHAT_ID:
			if '/pay'in msg.text:
				
				if len(msg.text.split()) == 1:
					return
				else:
					n = int(msg.text.split()[1])
					n = abs(n)

					t=datetime.date.today().strftime('%d.%m.%Y')
					bot.send_message(TO_CHAT_ID, f"Счет № {msg.message_id} от {t}\n\nПолучатель МАО ТУР (QIWI Банк)\n\nСумма для оплаты: <b>{n}</b> рублей.\n\n<a href='https://qiwi.com/payment/form/99999?amount={n}&extra[%27accountType%27]=nickname&extra[%27account%27]=MAOTUOR&extra[%27comment%27]=MaoTur&blocked[2]=comment&blocked[1]=account'>💳 Оплатить ⬅️</a>", parse_mode="HTML")
	
					bot.copy_message(message_id=msg.message_id+1,chat_id=msg.reply_to_message.	forward_from.id,from_chat_id=msg.chat.id)
					bot.send_message(TO_CHAT_ID, "Счет выставлен клиенту!")
					return
			

			bot.copy_message(message_id=msg.message_id,chat_id=msg.reply_to_message.forward_from.id,from_chat_id=msg.chat.id)
			bot.send_message(TO_CHAT_ID, "Сообщение клиенту отправлено!")
	else:
		
		bot.forward_message(TO_CHAT_ID, msg.chat.id, msg.message_id)
		bot.send_message(TO_CHAT_ID, f"От: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.first_name}</a> id: {msg.from_user.id}", parse_mode="HTML")
		
		bot.send_message(msg.chat.id, f"Обменник: {msg.from_user.first_name} ваш заказ на обработке.")
		main(msg)
		

		

# bot.polling(none_stop=True)

# Дальнейший код используется для установки и удаления вебхуков
server = Flask(__name__)


@server.route("/bot", methods=['POST'])
def get_message():
	""" TODO """
	decode_json = request.stream.read().decode("utf-8")
	bot.process_new_updates([telebot.types.Update.de_json(decode_json)])
	return "!", 200


@server.route("/")
def webhook_add():
	""" TODO """
	bot.remove_webhook()
	bot.set_webhook(url=config.url)
	return "!", 200

@server.route("/<password>")
def webhook_rem(password):
	""" TODO """
	password_hash = hashlib.md5(bytes(password, encoding="utf-8")).hexdigest()
	if password_hash == "5b4ae01462b2930e129e31636e2fdb68":
		bot.remove_webhook()
		return "Webhook removed", 200
	else:
		return "Invalid password", 200


server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
