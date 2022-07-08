#!usr/bin/python3
import datetime
import hashlib
import string
import os
from flask import Flask, request
import peewee as pw
import telebot

from database import Users
import config

TELEGRAM_API = os.environ["telegram_token"]
bot = telebot.TeleBot(TELEGRAM_API)
    
@bot.message_handler(commands=["start"])
def start(msg):
	bot.send_message(msg.chat.id, "<b>МАО-ТУР</b>\n\n✅ Индивидуальные туры\n✅ Экскурсии\n✅ Трансфер\n✅ Проживание\n\nКомпания МАО ТУР - ориентирована на максимально активный отдых. С большим опытом и заботой для Вас, организовывает экскурсии и индивидуальные туры по Абхазии!",parse_mode="HTML")
	main(msg)
	
		
@bot.message_handler(commands=["main"])
def main(msg):
	keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	khvtrip = telebot.types.KeyboardButton(text="🚕 Трансфер")
	servise = telebot.types.KeyboardButton(text="ℹ️ О компании")
	newsadd = telebot.types.KeyboardButton(text="🏖 Экскурсии")
	loveadd = telebot.types.KeyboardButton(text="🏠️ Жилье")
	tel = telebot.types.KeyboardButton(text="☎️ Звонок")
	keyboard.add( newsadd, loveadd, khvtrip, servise,tel)
	bot.send_message(msg.chat.id, "Задать вопрос ⬇️", reply_markup=keyboard)
	
	selected_user = Users.select().where(
		Users.userid == msg.from_user.id)
	if not selected_user:
		insert_user(msg.from_user)

def insert_user(user):
	new_user = Users.create(
				userid=user.id)
	new_user.save()

@bot.message_handler(commands=["dom"])
def addlove(msg):
	chanel ="<b>Аренда жилья️</b>\n\n• Комнаты\n• Квартиры\n• Апартаменты\n• Гостевые дома"
	markup = telebot.types.InlineKeyboardMarkup()
	button = telebot.types.InlineKeyboardButton(text="Каталог апартаментов", url="https://vk.com/market-67677674?section=album_10") 
	markup.add(button)
	bot.send_photo(msg.chat.id, f"https://telegra.ph/file/1fbe01e96aea7ef0aeb7e.png",caption=f"{chanel}️", parse_mode="HTML",reply_markup=markup)
	

@bot.message_handler(commands=["taxi"])
def khvtrip(msg):
	chanel ="Встретим и привезем. Стоимость трансфера - от 1000р."
	markup = telebot.types.InlineKeyboardMarkup()
	button = telebot.types.InlineKeyboardButton(text="Заказать трансфер", url="https://vk.com/mao_tour?w=product-67677674_7618425") 
	markup.add(button)
	
	bot.send_photo(msg.chat.id, f"https://telegra.ph/file/33c8b53bf724ed16e8763.png",caption=f"{chanel}️", parse_mode="HTML",reply_markup=markup)
	
@bot.message_handler(commands=["about"])
def about(msg):
	chanel ="Компания МАО ТУР - ориентирована на максимально активный отдых. С большим опытом и заботой для Вас, организовывает экскурсии и индивидуальные туры по Абхазии!"
	
	bot.send_photo(msg.chat.id, f"https://telegra.ph/file/9e773eb447e1899938642.png",caption=f"{chanel}️", parse_mode="HTML")

	
@bot.message_handler(commands=["tours"])
def addnews(msg):
	chanel ="<b>Туры и экскурсии</b>\n\n• Скальный монастырь Отхара + Форелевое хозяйство\n\n• Горячие источники + Парк Львов\n\n• Конные прогулки к водопадам\n\n• Джип тур - Гегский водопад +оз.Рица + Перевал Пыв\n\n• Джип тур на г. Мамзышха + 3 смотровые площадки\n\n• Тур на оз. Рица + оз. Малая Рица\n\n• Джип тур на Гегский водопад + оз. Рица\n\n• Тур по трём смотровым площадкам г.Гагра\n\n• Заброшенный город Акармара + 3 водопада + Горячий источник Кындык\n\n• Тур в Хашупсинский каньон + Белые скалы\n\n• Тур в Пицунду + Мюссерский заповедник\n\n• Тур на озеро Рица\n\n• Тур в Новый Афон\n\n• Тур в Черниговку + Кындык"
	markup = telebot.types.InlineKeyboardMarkup()
	button = telebot.types.InlineKeyboardButton(text="Заказать тур", url="https://vk.com/market-67677674?section=album_11") 
	markup.add(button)
	bot.send_photo(msg.chat.id, f"https://telegra.ph/file/1a3b65f2fd070569f5760.png",caption=f"{chanel}️", parse_mode="HTML",reply_markup=markup)
	
def tel(msg):
	bot.send_message(msg.chat.id, "Оставьте номер телефона. Оператор свяжется с вами в ближайшее время ⬇", parse_mode="HTML")


@bot.message_handler(commands=["serv","help"])
def serv(msg):
	markup = telebot.types.InlineKeyboardMarkup()
	button1 = telebot.types.InlineKeyboardButton(text="О компании", callback_data="О компании") 
 

	markup.add(button3, button1,button5, button2, button4, button6,button7,button8)
	bot.send_message(chat_id=msg.chat.id, text="В Абхазии:️", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: True)
def longname(call):
	a = datetime.datetime.today()
	if call.data == "О компании":
		bot.send_message(call.message.chat.id, f"<a href='https://khabara.ru/weather.html?{a}'>🌡</a>", parse_mode="HTML")
		


@bot.message_handler(commands=["stat"])
def stat(msg):

	count = Users.select().count()
	bot.send_message(msg.chat.id, count, parse_mode="HTML")

@bot.message_handler(commands=["s"])
def send(msg):

	if len(msg.text.split()) == 1:
		return
	selected_user = Users.select() 

	for i,user in enumerate(selected_user):
		try:
			if i % 20 == 0:
				time.sleep(1)
			bot.send_message(user.userid, msg.text[2:], parse_mode="HTML" )
		except:
			continue



	
@bot.message_handler(commands=["trip"])
def donate(msg):
	markup = telebot.types.InlineKeyboardMarkup()
	button = telebot.types.InlineKeyboardButton(text='🏖 Заказать', url="https://t.me/abhaziabot")
	markup.add(button)
	
	bot.edit_message_text(
	chat_id=-1001787255599,
	message_id=6,
	text="ℹ️ Компания МАО ТУР - ориентирована на максимально активный отдых. С большим опытом и заботой для Вас, организовывает экскурсии и индивидуальные туры по Абхазии!\n\nЭкскурсии, Жилье, Трансфер...", parse_mode="HTML", reply_markup=markup)
    
@bot.message_handler(content_types=['text', 'document', 'photo', 'audio', 'video','voice'])
def all_messages(msg):
	TO_CHAT_ID= -1001378480179
		
	if msg.text == "🏖 Экскурсии":
		addnews(msg)
		return
	if msg.text == "ℹ️ О компании":
		about(msg)
		return
	if msg.text == "🏠️ Жилье":
		addlove(msg)
		return


	if msg.text == "🚕 Трансфер":
		khvtrip(msg)
		return
	if msg.text == "☎️ Звонок":
		tel(msg)
		return
		

	if msg.chat.id == TO_CHAT_ID:

			bot.copy_message(message_id=msg.message_id,chat_id=msg.reply_to_message.forward_from.id,from_chat_id=msg.chat.id)
			bot.send_message(TO_CHAT_ID, "Сообщение клиенту отправлено!")
	else:
		
		bot.forward_message(TO_CHAT_ID, msg.chat.id, msg.message_id)
		bot.send_message(TO_CHAT_ID, f"От: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.first_name}</a> id: {msg.from_user.id}", parse_mode="HTML")
		
		bot.send_message(msg.chat.id, f"МАО-ТУР: {msg.from_user.first_name} ваше сообщение получено.")
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
