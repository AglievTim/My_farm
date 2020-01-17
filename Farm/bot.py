import telebot
import sqlite3
from threading import Thread
from time import sleep
from markdown import Markdown
from config import *
from keyboards import *
from animals_in_game import *
from buttons import Buttons
from database import DataBase
from functions import Functions

con = sqlite3.connect(DATA, check_same_thread = False)
bot = telebot.TeleBot(TOKEN)

bt = Buttons()
db = DataBase()
func = Functions()

db.create_table_market_prices()
db.create_table()
db.add_start_prices()

@bot.message_handler(commands = ['start'])
def start_message(message):
	db.add_new_gamer(message.from_user.id, DATA)
	bot.send_message(message.chat.id, f"Привет, {message.from_user.username}, рады видеть тебя на ферме.", reply_markup = main)


@bot.message_handler(func = lambda message: message.text == bt.farm)
def farm(message):
	func.information_about_farm(message.chat.id, message.from_user.id)
@bot.message_handler(func = lambda message: message.text == bt.animals)
def shop(message):
	bot.send_message(message.chat.id, 
		
			"*Купить животных*\n\n"
			'В этом разделе вы можете приобрести животных.\n'
			'Животные будут производить ресурсы,'
			'которые вам необхадимо собирать на ферме.\n'
			'Собранные ресурсы можно будет продать на рынке,'
			'а заработанные деньги вы можете потратить на новых животных '
			'или же вывести себе на кошелек.', 
			parse_mode = 'Markdown', reply_markup = inline_buttons_animals

		)
	
@bot.message_handler(func = lambda message: message.text == bt.mart)
def mart(message):
	market_rate = db.take_mart().fetchone()
	bot.send_message(message.chat.id,

			'*Рынок*\n\n'
			'Рынок - это то место, где вы можете продать, произведенные вашими животными, ресурсы.\n'
			'Обратите внимание, что цены на рынке меняются каждые пять часов, воспользуйтесь этим для извлчения наибольшей прибыли!\n'
			'*Текущий курс:*\n\n'
			f'🥚 - {market_rate[0]}\n'
			f'💭 - {market_rate[1]}\n'
			f'🥛 - {market_rate[2]}\n'
			f'🥩 - {market_rate[3]}\n',

			parse_mode = 'Markdown', reply_markup = inline_for_sale_products

		)
@bot.message_handler(func = lambda message: message.text == bt.angar)
def angar(message):
	print("Склад")


@bot.callback_query_handler(func=lambda call: True)
def show_animals_shop(call):
	user_id = call.from_user.id
	chat_id = call.message.chat.id
	#Отображение информации о животных в магазине
	if call.data == 'buy_animals':
		func.send_description_animal(chat_id, chicken, inline_button_buy_chicken)
		func.send_description_animal(chat_id, sheep, inline_button_buy_sheep)
		func.send_description_animal(chat_id, cow, inline_button_buy_cow)
		func.send_description_animal(chat_id, pig, inline_button_buy_pig)
	#Обработка нажатия клавишы "Купить" в магазине
	if call.data == 'buy_chicken':
		Thread(target = func.action_after_purchase, args = (chicken, user_id, chat_id,)).start()
	if call.data == 'buy_sheep':
		func.action_after_purchase(sheep, user_id, chat_id)
	if call.data == 'buy_cow':
		func.action_after_purchase(cow, user_id, chat_id)
	if call.data == 'buy_pig':
		func.action_after_purchase(pig, user_id, chat_id)
	if call.data == 'my_animals':
		func.information_about_farm(chat_id, user_id)


Thread(target = func.main).start()


if __name__ == '__main__':
	bot.polling(none_stop = True)

		