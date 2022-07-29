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
	khvtrip = telebot.types.KeyboardButton(text="🚕\nТрансфер")
	servise = telebot.types.KeyboardButton(text="ℹ️ Мао-Тур")
	newsadd = telebot.types.KeyboardButton(text="🏖\nЭкскурсии")
	newsadd2 = telebot.types.KeyboardButton(text="🔥\nЭксклюзив")
	loveadd = telebot.types.KeyboardButton(text="🏠️ Жилье")
	tel = telebot.types.KeyboardButton(text="☎️ Звонок")
	keyboard.add( newsadd, newsadd2, khvtrip, loveadd, servise,tel)
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
	main(msg)
	

@bot.message_handler(commands=["taxi"])
def khvtrip(msg):
	chanel ="Встретим и привезем. Стоимость трансфера - от 1000р."
	markup = telebot.types.InlineKeyboardMarkup()
	button = telebot.types.InlineKeyboardButton(text="Заказать трансфер", callback_data="taxi") 
	markup.add(button)
	
	bot.send_photo(msg.chat.id, f"https://telegra.ph/file/33c8b53bf724ed16e8763.png",caption=f"{chanel}️", parse_mode="HTML",reply_markup=markup)
	main(msg)
	
@bot.message_handler(commands=["about"])
def about(msg):
	chanel ="Компания МАО-ТУР - ориентирована на максимально активный отдых. С большим опытом и заботой для Вас, организовывает экскурсии и индивидуальные туры по Абхазии!\n\n<b>Контакты:</b>\n+7 (940) 713-16-57\nTelegram: @mao_tour\nInsta: instagram.com/mao_tour\nВК: vk.com/mao_tour\nОК: ok.ru/maotour"
	
	bot.send_photo(msg.chat.id, f"https://telegra.ph/file/42450df7fb04d4b819958.jpg",caption=f"{chanel}️", parse_mode="HTML")
	main(msg)

	
@bot.message_handler(commands=["tours"])
def addnews(msg):
	chanel ="<b>Туры и экскурсии</b>\n\n• Заброшенный город Акармара + 3 водопада + Горячий источник Кындыг\n\n• Джип тур на Гегский водопад + оз. Рица\n\n• Конные прогулки к водопадам\n\n• Тур на озеро Рица\n\n• Джип тур - Гегский водопад +оз.Рица+ Перевал Пыв\n\n• Пляж с белыми скалами + смотровая на закате + Хурмовая роща\n\n• Джип тур на г. Мамзышха + 3 смотровые площадки\n\n• Парк Львов+скальный монастырь Отхара + форелевая ферма\n\n• Тур на оз. Рица + оз. Малая Рица\n\n• Тур по трём смотровым площадкам г.Гагра\n\n• Тур в Хашупсинский каньон + Белые скалы\n\n• Тур в Новый Афон\n\n• Тур в Пицунду + Мюссерский заповедник\n\n• Тур в Черниговку + Кындыг"
	markup = telebot.types.InlineKeyboardMarkup()
	button = telebot.types.InlineKeyboardButton(text="Заказать тур", callback_data="tours") 
	markup.add(button)
	bot.send_photo(msg.chat.id, f"https://telegra.ph/file/1a3b65f2fd070569f5760.png",caption=f"{chanel}️", parse_mode="HTML",reply_markup=markup)
	main(msg)
	
@bot.message_handler(commands=["vip"])
def addnews2(msg):
	chanel ="<b>Уникальный отдых</b>\n\n• Полёт на параплане в Абхазии\n\n• Алко-Пати на лимузине"
	markup = telebot.types.InlineKeyboardMarkup()
	button = telebot.types.InlineKeyboardButton(text="Заказать тур", callback_data="tours2") 
	markup.add(button)
	bot.send_photo(msg.chat.id, f"https://telegra.ph/file/1ed90785675dfb4eedfe8.jpg",caption=f"{chanel}️", parse_mode="HTML",reply_markup=markup)
	main(msg)
	
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
	if call.data == "tours2":
		bot.send_message(call.message.chat.id, f"Оставьте номер телефона. Оператор свяжется с вами в ближайшее время ⬇️", parse_mode="HTML")
		return
	if call.data == "tours":
		bot.send_message(call.message.chat.id, f"Оставьте номер телефона. Оператор свяжется с вами в ближайшее время ⬇️", parse_mode="HTML")
		return
	if call.data == "taxi":
		bot.send_message(call.message.chat.id, f"Оставьте номер телефона. Оператор свяжется с вами в ближайшее время ⬇️", parse_mode="HTML")
		return
		


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
	
	bot.edit_message_caption(
	chat_id=-1001787255599,
	message_id=5,
	caption="ℹ️ Индивидуальные экскурсии и авторские туры по Абхазии в малых группах по 4-6 чел от МАО тур.\n\n• Путешествия на комфортабельных минивэнах и джипах с бесплатным wi-fi, чтобы вы могли не только наслаждаться комфортной дорогой, но и быть всегда на связи и делиться историями в соц сетях.\n\n• Время для фото и прогулок - не ограничено. Вы можете хоть по часу фотографироваться с каждой достопримечательностью.\n\n• Мы забираем вас и привозим обратно из отеля или с границы, никаких точек сбора.\n\n• Всех наших клиентов мы угощаем вкуснейшим домашним вином. В каждой экскурсии заезжаем на бесплатную дегустацию сыра, мёда, вина, чачи.\n\nВсе что нужно для вашего комфортного отдыха - это отправить заявку!️", parse_mode="HTML", reply_markup=markup)
	return

@bot.message_handler(commands=["blog"])
def blog(msg):


	markup = telebot.types.InlineKeyboardMarkup()
	button = telebot.types.InlineKeyboardButton(text='Контакты', url=f"https://t.me/j_crush/13")
	markup.add(button)


	bot.edit_message_text(
	chat_id=-1001080261871,
	message_id=13,
	text="ℹ️ <b>Travel, Sport, Moneymaking</b>\
\n\nTelegram: @jcrush", parse_mode="HTML", reply_markup=markup)
	return
    
@bot.message_handler(content_types=['text', 'document', 'photo', 'audio', 'video','voice'])
def all_messages(msg):
	TO_CHAT_ID= -1001378480179
		
	if msg.text == "🏖\nЭкскурсии":
		addnews(msg)
		return
		
	if msg.text == "🔥\nЭксклюзив":
		addnews2(msg)
		return
		
	if msg.text == "ℹ️ Мао-Тур":
		about(msg)
		return
	if msg.text == "🏠️ Жилье":
		addlove(msg)
		return


	if msg.text == "🚕\nТрансфер":
		khvtrip(msg)
		return
	if msg.text == "☎️ Звонок":
		tel(msg)
		return
		

	if msg.chat.id == TO_CHAT_ID:
			if '/pay'in msg.text:
				
				if len(msg.text.split()) == 1:
					return
				else:
					n = int(msg.text.split()[1])
					n = abs(n)

	
					bot.send_message(TO_CHAT_ID, f"Счет <b>{n}</b> рублей.\n<a href='https://qiwi.com/payment/form/99999?amount={n}&extra[%27accountType%27]=nickname&extra[%27account%27]=MAOTUOR&extra[%27comment%27]=MaoTur&blocked[2]=comment&blocked[1]=account'>💳 Оплатить ⬅️</a>", parse_mode="HTML")
	
					bot.copy_message(message_id=msg.message_id+1,chat_id=msg.reply_to_message.	forward_from.id,from_chat_id=msg.chat.id)
					bot.send_message(TO_CHAT_ID, "Счет выставлен клиенту!")
					return
			

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
