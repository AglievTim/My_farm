import sqlite3
import random
from config import DATA, MARKET_PRICE, ANGAR_LEVELS
from animals_in_game import *


class DataBase:

	#Создаем таблицу с профилем игрока
	def create_table(event):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS profile_information(user_id INTEGER, balance INTEGER, chicken_count INTEGER, sheep_count INTEGER, cow_count INTEGER, pig_count INTEGER, eggs INTEGER, wool INTEGER, milk INTEGER, meat INTEGER, crib_status INTEGER, angar_level INTEGER)")
		con.close()
		
	def create_table_market_prices(event):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS market_prices(egg_price INTEGER, wool_price INTEGER, milk_price INTEGER, meat_price INTEGER)")
		con.close()

	#Добавляем начальные данные в таблицу с ценами рынка
	def add_start_prices(event):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		cursor.execute('INSERT INTO market_prices VALUES(?,?,?,?)', (MARKET_PRICE['egg'], MARKET_PRICE['wool'], MARKET_PRICE['milk'], MARKET_PRICE['meat']))
		con.commit()
		con.close()

	#Добавляем профиль нового игрока в таблицу
	def add_new_gamer(event, user_id, data):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		cursor.execute("INSERT INTO profile_information VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (user_id, 500000000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1))
		con.commit()
		con.close()

	#Возвращает баланс игрока
	def take_balance(event, user_id):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		balance = cursor.execute(f'SELECT balance FROM profile_information WHERE user_id = {user_id}').fetchone()[0]
		return balance
		con.close()

	#Вычитает баланс
	def minus_balance(event, user_id, sum):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		cursor.execute(f'UPDATE profile_information SET balance = balance - {sum} WHERE user_id = {user_id}')
		con.commit()
		con.close()

	#Увеличивает баланс
	def plus_balance(event, user_id, sum):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		cursor.execute(f'UPDATE profile_information SET balance = balance + {sum} WHERE user_id = {user_id}')
		con.commit()
		con.close()

	#Добавляет купленное животное
	def add_animal(event, user_id, animal):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		cursor.execute(f'UPDATE profile_information SET {animal} = {animal} + 1 WHERE user_id = {user_id}')
		con.commit()
		con.close()

	#Возвращает всех животных игрока
	def take_all_animals(event, user_id):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		all_animals = cursor.execute(f'SELECT chicken_count, sheep_count, cow_count, pig_count FROM profile_information WHERE user_id = {user_id}')
		return all_animals
		con.close()

	#Возвращает все ресурсы игрока
	def take_all_products(event, user_id):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		all_products = cursor.execute(f'SELECT eggs, wool, milk, meat FROM profile_information WHERE user_id = {user_id}')
		return all_products
		con.close()

	#Прибавляет ресурсы игроку
	def update_products(event, user_id, animal, angar_level, products):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		animal_count = cursor.execute(f'SELECT {animal.english_name}_count FROM profile_information WHERE user_id = {user_id}').fetchone()
		products_count = animal_count[0] * animal.performance
		product = ''

		if animal == chicken:
			product = 'eggs'
		if animal == sheep:
			product = 'wool'
		if animal == cow:
			product = 'milk'
		if animal == pig:
			product = 'meat'

	
		if (products + products_count) > ANGAR_LEVELS[angar_level]:
			cursor.execute(f'UPDATE profile_information SET {product} = {ANGAR_LEVELS[angar_level]} WHERE user_id = {user_id}')
		else:				
			cursor.execute(f'UPDATE profile_information SET {product} = {product} + {animal.english_name}_count * {animal.performance} WHERE user_id = {user_id}')

	
		con.commit()
		con.close()

			

	#Изменение рынка
	def change_mart(event):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()

		egg_price_random = random.randint(MARKET_PRICE['egg'],int(MARKET_PRICE['egg'] * 1.25))
		wool_price_random = random.randint(MARKET_PRICE['wool'], int(MARKET_PRICE['wool'] * 1.25))
		milk_price_random = random.randint(MARKET_PRICE['milk'], int(MARKET_PRICE['milk'] * 1.25))
		meat_price_random = random.randint(MARKET_PRICE['meat'], int(MARKET_PRICE['meat'] * 1.25))

		cursor.execute(f'UPDATE market_prices SET egg_price = {egg_price_random}')
		cursor.execute(f'UPDATE market_prices SET wool_price = {wool_price_random}')
		cursor.execute(f'UPDATE market_prices SET milk_price = {milk_price_random}')
		cursor.execute(f'UPDATE market_prices SET meat_price = {meat_price_random}')
		con.commit()
		con.close()	

	#Возвращает курс рынка
	def take_mart(event):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		market_rate = cursor.execute('SELECT egg_price, wool_price, milk_price, meat_price FROM market_prices')
		return market_rate
		con.close()
	
	#Количество продутков у человека
	def product_sum(event, user_id, animal):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		all_products = cursor.execute(f'SELECT eggs, wool, milk, meat FROM profile_information WHERE user_id = {user_id}').fetchone()
		responce = 0

		if animal == chicken:
			responce = all_products[0]
		if animal == sheep:
			responce = all_products[1]
		if animal == cow:
			responce = all_products[2]
		if animal == pig:
			responce = all_products[3]
		return responce
		con.close()

	#Возвращает уровень хлева
	def angar_level(event, user_id):
		con = sqlite3.connect(DATA, check_same_thread = False)
		cursor = con.cursor()
		level = cursor.execute(f'SELECT angar_level FROM profile_information WHERE user_id = {user_id}').fetchone()
		return level[0]
		con.close()




			


