import telebot
import schedule
from markdown import Markdown
from config import *
from animals_in_game import *
from database import DataBase
from time import sleep


bot = telebot.TeleBot(TOKEN)

db = DataBase()


class Functions:
	#Обрабатывает нажатие на кнопку покупки
	def action_after_purchase(event, animal, user_id, chat_id):
		if db.take_balance(user_id) >= animal.price:
			db.minus_balance(user_id, animal.price)
			db.add_animal(user_id, str(animal.english_name) + '_count')
			bot.send_message(chat_id,
				'🎉 *Ура!*\n\n'
				'Поздравляем тебя с приобритением нового животного.',
				parse_mode = 'Markdown'

				)
		else:
			bot.send_message(chat_id, 
				'🤔*Хм...*\n\n'
				'Кажется вам не хватает денег для покупки этого животного.\n'
				f'*{animal.name}* стоит *{animal.price}* 💰, а у вас на счету всего *{db.take_balance(user_id)}* 💰', 
				parse_mode = 'Markdown'
				)
	#Выводит описание животного в магазине
	def send_description_animal(event, chat_id, animal, button):
		bot.send_photo(chat_id, open(animal.picture, 'rb'), 
			f'*{animal.name}*\n\n'
			f'Цена: {animal.price}\n'
			f'Добывает: {animal.performance} {animal.product} в час'
			, parse_mode = 'Markdown', reply_markup = button
			)
	#Выводит информацию о ферме
	def information_about_farm(event, chat_id, user_id):
		all_animals = db.take_all_animals(user_id).fetchone()
		all_products = db.take_all_products(user_id).fetchone()
		bot.send_message(chat_id, 
		'*Ферма*\n\n'
		'Здесь обитают купленные вами животные.'
		' Они производят ресурсы, которые вы можете собирать и продавать на рынке.'
		'Ниже вы можете посмотреть сколько ресурсов произвели ваши животные с момента последнего сбора и собрать их.\n\n'

		f'*{chicken.name}*\n'
		f'Количество: {all_animals[0]}\n'
		f'Добыли: {all_products[0]} 🥚\n\n'

		f'*{sheep.name}*\n'
		f'Количество: {all_animals[1]}\n'
		f'Добыли: {all_products[1]} 💭\n\n'

		f'*{cow.name}*\n'
		f'Количество: {all_animals[2]}\n'
		f'Добыли: {all_products[2]} 🥛\n\n'

		f'*{pig.name}*\n'
		f'Количество: {all_animals[3]}\n'
		f'Добыли: {all_products[3]} 🥩\n\n',

		parse_mode = 'Markdown'
		)

	def main(event):
		schedule.every(10).seconds.do(db.update_products)
		schedule.every(50).seconds.do(db.change_mart)
			
		while True:
			schedule.run_pending()
			sleep(1)


			

