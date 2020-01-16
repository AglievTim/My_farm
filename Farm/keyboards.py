import telebot
from buttons import Buttons

bt = Buttons()
main = telebot.types.ReplyKeyboardMarkup(True)
main.row(bt.farm, bt.animals)
main.row(bt.mart, bt.angar)

go_main = telebot.types.ReplyKeyboardMarkup(True)
go_main.row(bt.back)

#Инлайн кнопки в разделе "Животные"
inline_buttons_animals = telebot.types.InlineKeyboardMarkup()

buy_animals = telebot.types.InlineKeyboardButton(text = bt.buy_animals, callback_data = 'buy_animals')
legendary_animals = telebot.types.InlineKeyboardButton(text = bt.legendary_animals, callback_data = 'legendary_animals')
my_animals = telebot.types.InlineKeyboardButton(text = bt.my_animals, callback_data = 'my_animals')

inline_buttons_animals.add(buy_animals)
inline_buttons_animals.add(legendary_animals)
inline_buttons_animals.add(my_animals)

#Инлайн для курицы
inline_button_buy_chicken = telebot.types.InlineKeyboardMarkup()
buy_chicken = telebot.types.InlineKeyboardButton(text = bt.buy, callback_data = 'buy_chicken')

inline_button_buy_chicken.add(buy_chicken)

#Инлайн для овцы
inline_button_buy_sheep = telebot.types.InlineKeyboardMarkup()
buy_sheep = telebot.types.InlineKeyboardButton(text = bt.buy, callback_data = 'buy_sheep')

inline_button_buy_sheep.add(buy_sheep)

#Инлайн для коровы
inline_button_buy_cow = telebot.types.InlineKeyboardMarkup()
buy_cow = telebot.types.InlineKeyboardButton(text = bt.buy, callback_data = 'buy_cow')

inline_button_buy_cow.add(buy_cow)

#Инлайн для свиньи
inline_button_buy_pig = telebot.types.InlineKeyboardMarkup()
buy_pig = telebot.types.InlineKeyboardButton(text = bt.buy, callback_data = 'buy_pig')

inline_button_buy_pig.add(buy_pig)

#Инлайн для продажи ресурсов
inline_for_sale_products = telebot.types.InlineKeyboardMarkup()

sale_egg = telebot.types.InlineKeyboardButton(text = bt.sale_egg, callback_data = bt.sale_egg)
sale_wool = telebot.types.InlineKeyboardButton(text = bt.sale_wool, callback_data = bt.sale_wool)
sale_milk = telebot.types.InlineKeyboardButton(text = bt.sale_milk, callback_data = bt.sale_milk)
sale_meat = telebot.types.InlineKeyboardButton(text = bt.sale_meat, callback_data = bt.sale_meat)

inline_for_sale_products.add(sale_egg)
inline_for_sale_products.add(sale_wool)
inline_for_sale_products.add(sale_milk)
inline_for_sale_products.add(sale_meat)
