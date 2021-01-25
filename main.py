import telebot
import os
import shutil
import time
import pickle
from config import TOKEN
from telebot.types import InputMediaPhoto
from telebot.types import LabeledPrice
from flask import Flask, request, jsonify


# WEBHOOK_HOST = '5.63.159.36'
# WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')

# WEBHOOK_URL_BASE = "https://%s:%s/bot" % (WEBHOOK_HOST, WEBHOOK_PORT)
# WEBHOOK_URL_PATH = "/%s/" % (TOKEN)
# print(WEBHOOK_URL_PATH)

bufer_photo = {}
bufer_text = {}
bufer_sum = {}
bufer_name  = {}
admin = [465112900]

#Клавиатура для админа
keyBoard_admin = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard = True)
#Клавиатура по завершению добавления
keyBoard_finish_add = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard = True)
#Клавиатура для проверки текста
keyBoard_verify = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard = True)
#Клавиатура для размещения поста
keyBoard_next_step = telebot.types.ReplyKeyboardMarkup(True)
#Клавиатура доставки
keyBoard_delivery = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard = True)
#Клавиатура доставки
keyBoard_pay = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard = True)


#Кнопки для админа
keyBoard_admin.row('Добавить пост')
#Кнопка по завершению добавления
keyBoard_finish_add.row('Закончить добавление')
#Кнопки для проверки текста/поста
keyBoard_verify.row('Текст введен верно')
keyBoard_verify.row('Изменить текст')
#Кнопки для размещения поста
keyBoard_next_step.row('Посмотеть пост перед отправкой')
keyBoard_next_step.row('Разместить пост')
keyBoard_next_step.row('Внести изменения')
#Кнопки доставки
keyBoard_delivery.row('Самовывоз📦')
keyBoard_delivery.row('Доставка🚚')
#Кнопка оплаты
keyBoard_pay.row('Подтвердить и оплатить')
keyBoard_pay.row('Изменить')

# app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)
# bot.remove_webhook()
# time.sleep(2)
# bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open('/ssl/bot_sert.pem', 'r'))

#Просмотр поста перед отправкой
def view_post(message):
    global bufer_text
    global bufer_photo

    tg_id = message.from_user.id

    count_photo = len(bufer_photo[tg_id])
    print(count_photo)
    # if count_photo == 1:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1:
    #         bot.send_photo(message.from_user.id, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb'), bufer_text[tg_id][0])
    # elif count_photo == 2:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2)]
    #         bot.send_media_group(message.from_user.id, files)
    # elif count_photo == 3:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2), InputMediaPhoto(f3)]
    #         bot.send_media_group(message.from_user.id, files)
    # elif count_photo == 4:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4)]
    #         bot.send_media_group(message.from_user.id, files)
    # elif count_photo == 5:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][4]}', 'rb') as f5:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4), InputMediaPhoto(f5)]
    #         bot.send_media_group(message.from_user.id, files)
    # elif count_photo == 6:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][4]}', 'rb') as f5, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][5]}', 'rb') as f6:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4), InputMediaPhoto(f5),\
    #                  InputMediaPhoto(f6)]
    #         bot.send_media_group(message.from_user.id, files)
    # elif count_photo == 7:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][4]}', 'rb') as f5, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][5]}', 'rb') as f6,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][6]}', 'rb') as f7:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4), InputMediaPhoto(f5),\
    #                  InputMediaPhoto(f6), InputMediaPhoto(f7)]
    #         bot.send_media_group(message.from_user.id, files)
    # elif count_photo == 8:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][4]}', 'rb') as f5, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][5]}', 'rb') as f6,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][6]}', 'rb') as f7, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][7]}', 'rb') as f8:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4), InputMediaPhoto(f5),\
    #                  InputMediaPhoto(f6), InputMediaPhoto(f7), InputMediaPhoto(f8)]
    #         bot.send_media_group(message.from_user.id, files)
    # elif count_photo == 9:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][4]}', 'rb') as f5, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][5]}', 'rb') as f6,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][6]}', 'rb') as f7, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][7]}', 'rb') as f8,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][8]}', 'rb') as f9:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4), InputMediaPhoto(f5),\
    #                  InputMediaPhoto(f6), InputMediaPhoto(f7), InputMediaPhoto(f8),\
    #                  InputMediaPhoto(f9)]
    #         bot.send_media_group(message.from_user.id, files)
    # elif count_photo == 10:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][4]}', 'rb') as f5, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][5]}', 'rb') as f6,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][6]}', 'rb') as f7, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][7]}', 'rb') as f8,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][8]}', 'rb') as f7, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][9]}', 'rb') as f10:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4), InputMediaPhoto(f5),\
    #                  InputMediaPhoto(f6), InputMediaPhoto(f7), InputMediaPhoto(f8),\
    #                  InputMediaPhoto(f9), InputMediaPhoto(f10)]
    #         bot.send_media_group(message.from_user.id, files)
#Отправка поста на канал
def send_post(message):
    global bufer_text
    global bufer_photo
    global bufer_sum
    global bufer_name
    
    tg_id = message.from_user.id
    
    with open('DB/bouquets.pickle', 'rb') as f:
        bouquets = pickle.load(f)
    
    num_post = str(len(bouquets) + 1)
    print(num_post)
    bouquets[num_post] = []
    bouquets[num_post].append(bufer_sum[tg_id][0])
    bouquets[num_post].append(bufer_name[tg_id][0])
    with open('DB/bouquets.pickle', 'wb') as f:
        pickle.dump(bouquets,f)
    print(bouquets)

    keyBoard_post = telebot.types.InlineKeyboardMarkup(True)
    key_pay = telebot.types.InlineKeyboardButton(text=f'Купить: {bufer_sum[tg_id][0]}руб', url= f'https://t.me/florico_sale_bot?start={num_post}')
    key_feedback = telebot.types.InlineKeyboardButton(text='Обратная связь', url = 'https://t.me/floricom')
    key_catalog = telebot.types.InlineKeyboardButton(text='Перейти на сайт', url = 'https://florico.ru/')

    keyBoard_post.add(key_pay ,key_feedback, key_catalog)

    keyBoard_sale = telebot.types.InlineKeyboardMarkup(True)
    key_sale = telebot.types.InlineKeyboardButton(text='Продано', callback_data=f'''sale_{num_post}''')

    keyBoard_sale.add(key_sale)
 
    count_photo = len(bufer_photo[tg_id])
    print(count_photo)
    # if count_photo == 1:
    #     bot.send_photo(-1001475019288, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb'), bufer_text[tg_id][0])
    #     bot.send_message(-1001475019288, '''Вы можете приобрести букет, перейти на сайт или связаться с продавцом''', reply_markup = keyBoard_post)
    # elif count_photo == 2:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2)]
    #         bot.send_media_group(-1001475019288, files)
    #         bot.send_message(-1001475019288, '''Вы можете приобрести букет, перейти на сайт или связаться с продавцом''', reply_markup = keyBoard_post)
    # elif count_photo == 3:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2), InputMediaPhoto(f3)]
    #         bot.send_media_group(-1001475019288, files)
    #         bot.send_message(-1001475019288, '''Вы можете приобрести букет, перейти на сайт или связаться с продавцом''', reply_markup = keyBoard_post)
    # elif count_photo == 4:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4)]
    #         bot.send_media_group(-1001475019288, files)
    #         bot.send_message(-1001475019288, '''Вы можете приобрести букет, перейти на сайт или связаться с продавцом''', reply_markup = keyBoard_post)
    # elif count_photo == 5:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][4]}', 'rb') as f5:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4), InputMediaPhoto(f5)]
    #         bot.send_media_group(-1001475019288, files)
    #         bot.send_message(-1001475019288, '''Вы можете приобрести букет, перейти на сайт или связаться с продавцом''', reply_markup = keyBoard_post)
    # elif count_photo == 6:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][4]}', 'rb') as f5, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][5]}', 'rb') as f6:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4), InputMediaPhoto(f5),\
    #                  InputMediaPhoto(f6)]
    #         bot.send_media_group(-1001475019288, files)
    #         bot.send_message(-1001475019288, '''Вы можете приобрести букет, перейти на сайт или связаться с продавцом''', reply_markup = keyBoard_post)
    # elif count_photo == 7:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][4]}', 'rb') as f5, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][5]}', 'rb') as f6,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][6]}', 'rb') as f7:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4), InputMediaPhoto(f5),\
    #                  InputMediaPhoto(f6), InputMediaPhoto(f7)]
    #         bot.send_media_group(-1001475019288, files)
    #         bot.send_message(-1001475019288, '''Вы можете приобрести букет, перейти на сайт или связаться с продавцом''', reply_markup = keyBoard_post)
    # elif count_photo == 8:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][4]}', 'rb') as f5, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][5]}', 'rb') as f6,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][6]}', 'rb') as f7, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][7]}', 'rb') as f8:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4), InputMediaPhoto(f5),\
    #                  InputMediaPhoto(f6), InputMediaPhoto(f7), InputMediaPhoto(f8)]
    #         bot.send_media_group(-1001475019288, files)
    #         bot.send_message(-1001475019288, '''Вы можете приобрести букет, перейти на сайт или связаться с продавцом''', reply_markup = keyBoard_post)
    # elif count_photo == 9:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][4]}', 'rb') as f5, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][5]}', 'rb') as f6,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][6]}', 'rb') as f7, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][7]}', 'rb') as f8,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][8]}', 'rb') as f9:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4), InputMediaPhoto(f5),\
    #                  InputMediaPhoto(f6), InputMediaPhoto(f7), InputMediaPhoto(f8),\
    #                  InputMediaPhoto(f9)]
    #         bot.send_media_group(-1001475019288, files)
    #         bot.send_message(-1001475019288, '''Вы можете приобрести букет, перейти на сайт или связаться с продавцом''', reply_markup = keyBoard_post)
    # elif count_photo == 10:
    #     with open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][0]}', 'rb') as f1, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][1]}', 'rb') as f2,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][2]}', 'rb') as f3, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][3]}', 'rb') as f4,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][4]}', 'rb') as f5, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][5]}', 'rb') as f6,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][6]}', 'rb') as f7, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][7]}', 'rb') as f8,\
    #     open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][8]}', 'rb') as f7, open(f'photos_{message.from_user.id}/{bufer_photo[tg_id][9]}', 'rb') as f10:
    #         files = [InputMediaPhoto(f1, caption = f'{bufer_text[tg_id][0]}'),InputMediaPhoto(f2),\
    #                  InputMediaPhoto(f3), InputMediaPhoto(f4), InputMediaPhoto(f5),\
    #                  InputMediaPhoto(f6), InputMediaPhoto(f7), InputMediaPhoto(f8),\
    #                  InputMediaPhoto(f9), InputMediaPhoto(f10)]
    #         bot.send_media_group(-1001475019288, files)
    #         bot.send_message(-1001475019288, '''Вы можете приобрести букет, перейти на сайт или связаться с продавцом''', reply_markup = keyBoard_post)
    message_id = bot.send_message(-1001475019288, '''Вы можете приобрести букет, перейти на сайт или связаться с продавцом''', reply_markup = keyBoard_post).message_id
    for administrator in admin:
        message_admin = bot.send_message(administrator, '''Если все товары из категории выше проданы нажмите кнопку''', reply_markup = keyBoard_sale).message_id

    with open('DB/bouquets.pickle', 'rb') as f:
        bouquets = pickle.load(f)
    
    bouquets[num_post].append(message_id)
    bouquets[num_post].append(message_admin)
    with open('DB/bouquets.pickle', 'wb') as f:
        pickle.dump(bouquets,f)
    print(bouquets)


    shutil.rmtree(f'photos_{message.from_user.id}/')
    bufer_photo.pop(tg_id)
    bufer_text.pop(tg_id)
    bufer_sum.pop(tg_id)
    bufer_name.pop(tg_id)

def append_sum(message):
    tg_id = message.from_user.id
    try:
        user_text = int(message.text)
        bufer_sum[tg_id] = []
        bufer_sum[tg_id].append(user_text)
        print(bufer_sum)
        bot.reply_to(message, f'Вы ввели сумму равную {bufer_sum[tg_id][0]}. Введите название букета')
        bot.register_next_step_handler(message,append_name)
    except Exception as e:
        print(e)
        error = bot.send_message(message.from_user.id, '[ERROR]: Возникла ошибка попробуйте еще раз')
        bot.register_next_step_handler(error, append_sum)

def append_name(message):
    tg_id = message.from_user.id
    try:
        name_of_bouquets = message.text
        bufer_name[tg_id] = []
        bufer_name[tg_id].append(name_of_bouquets)
        print(bufer_name)
        bot.reply_to(message, f'Название букета принято', reply_markup = keyBoard_next_step)
    except Exception as e:
        print(e)
        error = bot.send_message(message.from_user.id, '[ERROR]: Возникла ошибка попробуйте еще раз')
        bot.register_next_step_handler(error, append_name)

#Текст поста
def append_text_accept(message):
    tg_id = message.from_user.id
    try:
        user_text = message.text
        bufer_text[tg_id] = []
        bufer_text[tg_id].append(user_text)
        print(bufer_text)
        bot.reply_to(message, 'Проверьте текст который вы хотите внести в пост', 
                    reply_markup = keyBoard_verify)
    except Exception as e:
        print(e)
        error = bot.send_message(message.from_user.id, '[ERROR]: Возникла ошибка попробуйте еще раз')
        bot.register_next_step_handler(error, append_text_accept)  

@bot.message_handler(content_types = ['photo'])
def append_photo_accept(message):
    tg_id = message.from_user.id
    try:
        if len(bufer_photo[tg_id]) == 10:
            bot.send_message(message.from_user.id, '''!!!Лимит фото превышен!!!
Нажмите кнопку чтобы перейти к следующему шару''', reply_markup = keyBoard_finish_add)
        else:
            file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = f'photos_{message.from_user.id}/' + file_info.file_path.split('/')[-1]
            with open(src, 'wb') as new_file:
               new_file.write(downloaded_file)

            bufer_photo[tg_id].append(file_info.file_path.split('/')[-1])
            print(bufer_photo)
            bot.reply_to(message, f'''Фото добавлено, если хотите добавить еще фото к посту просто отправьте мне его.
Количество фото в посте не должно превышать 10 штук.
Сейчас {len(bufer_photo[tg_id])}''',
                        reply_markup = keyBoard_finish_add)
    except Exception as e:
        print(e)
        error = bot.send_message(message.from_user.id, '[ERROR]: Возникла ошибка попробуйте еще раз')
        bot.register_next_step_handler(error, append_photo_accept) 
#Указание адреса доставки
def delivery(message):
    tg_id = message.from_user.id

    with open('DB/buyer.pickle', 'rb') as f:
        buyer = pickle.load(f)
    address = message.text
    buyer[tg_id].append(address)
    with open('DB/buyer.pickle', 'wb') as f:
        pickle.dump(buyer,f)
    bot.send_message(message.from_user.id, '''Пожалуйста, оставьте свой номер телефона, чтобы мы могли связяться с вами📱
Напишите телефон в формате "+79151343030"''')
    bot.register_next_step_handler(message, append_phone)

def append_phone(message):
    try:
        with open('DB/buyer.pickle', 'rb') as f:
            buyer = pickle.load(f)
        if message.text == "/start":
            bot.send_message(message.from_user.id, "Заказ отменен, выберите букет заново в @florico")
        else:
            phone = int(message.text)
            buyer[message.from_user.id].append(phone)
            with open('DB/buyer.pickle', 'wb') as f:
                pickle.dump(buyer,f)
            confirmation(message.from_user.id)
    except Exception as e:
        error = bot.send_message(message.from_user.id, '[ERROR]: Неверный формат. Повторите попытку или отправьте /start для выхода')
        bot.register_next_step_handler(error, append_phone)
#Подтверждение правильности заказа
def confirmation(tg_id):
    with open('DB/buyer.pickle', 'rb') as f:
        buyer = pickle.load(f)
    with open('DB/bouquets.pickle', 'rb') as f:
        bouquets = pickle.load(f)
    print(buyer)
    bot.send_message(tg_id, f'''Ваш заказ, "{bouquets[buyer[tg_id][0]][1]}", стоимостью {bouquets[buyer[tg_id][0]][0]}руб.
Выбранный вариант доставки: {buyer[tg_id][1]}
Адрес доставки: {buyer[tg_id][2]}
Ваш номер телефона: +{buyer[tg_id][3]}''', reply_markup = keyBoard_pay)

#Оплата букета
def buy_flower(tg_id):
    with open('DB/buyer.pickle', 'rb') as f:
        buyer = pickle.load(f)
    with open('DB/bouquets.pickle', 'rb') as f:
        bouquets = pickle.load(f)

    bot.send_invoice(
                    chat_id = tg_id,
                    need_name = True,
                    need_phone_number = True,
                    title = f'Оплата заказа!!!',
                    description = f'''Ваш заказ, "{bouquets[buyer[tg_id][0]][1]}", стоимостью {bouquets[buyer[tg_id][0]][0]}руб.
Выбранный вариант доставки: {buyer[tg_id][1]}
Адрес доставки: {buyer[tg_id][2]}''',
                    invoice_payload = 'true',
                    provider_token = '390540012:LIVE:12147',
                    start_parameter = 'true',
                    currency = 'RUB',
                    prices = [LabeledPrice(label=f'"{bouquets[buyer[tg_id][0]][1]}"', amount = int(f'''{bouquets[buyer[tg_id][0]][0]}00'''))]
                    )

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    # print(message)
    tg_id = message.from_user.id
    bot.send_message(tg_id,'''Ваш платеж успешно дошел, спасибо за оплату!
С вами свяжется наш оператор. Также если есть какие либо вопросы можете писать сюда: @floricom''', reply_markup = None)

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(query):
    tg_id = query.from_user.id
    with open('DB/buyer.pickle', 'rb') as f:
        buyer = pickle.load(f)
    with open('DB/bouquets.pickle', 'rb') as f:
        bouquets = pickle.load(f)
    print(query)
    bot.answer_pre_checkout_query(query.id, ok=True)  
    #Сообщение после оплаты для продавца
    for administrator in admin:
        bot.send_message(administrator, f'''Пользователь {query.order_info.name} (@{query.from_user.username}) оплатил заказ "{bouquets[buyer[tg_id][0]][1]}"
Выбранный вариант доставки: {buyer[tg_id][1]}
Адрес доставки: {buyer[tg_id][2]}
Контактная информация:
телефон - {query.order_info.phone_number}''')
    buyer.pop(tg_id)


# @app.route(f'{WEBHOOK_URL_PATH}', methods=['POST'])
# def getMessage():
#         bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#         return "ok", 200
@bot.callback_query_handler(func=lambda call: True)
def sale(call):
    with open('DB/bouquets.pickle', 'rb') as f:
        bouquets = pickle.load(f)

    keyBoard_post_sale = telebot.types.InlineKeyboardMarkup(True)
    key_feedback = telebot.types.InlineKeyboardButton(text='Обратная связь', url = 'https://t.me/floricom')
    key_catalog = telebot.types.InlineKeyboardButton(text='Перейти на сайт', url = 'https://florico.ru/')

    keyBoard_post_sale.add(key_feedback, key_catalog)

    if call.data.split('_')[0] == 'sale':
        print(call.data)
        bot.edit_message_text(chat_id = -1001475019288, message_id = bouquets[call.data.split('_')[1]][2], text='Вы можете перейти на сайт или связаться с продавцом', reply_markup = keyBoard_post_sale)
        bot.edit_message_text(chat_id = call.from_user.id, message_id = bouquets[call.data.split('_')[1]][3], text='Все товары проданы!', reply_markup = None)



@bot.message_handler(commands = ['start'])
def start(message):
    tg_id = message.from_user.id
    
    with open('DB/admin.pickle', 'rb') as f:
        admin = pickle.load(f)
    with open('DB/buyer.pickle', 'rb') as f:
        buyer = pickle.load(f)
    with open('DB/bouquets.pickle', 'rb') as f:
        bouquets = pickle.load(f)
    
    print(message.from_user.id)
    if message.from_user.id in admin:
        bot.send_message(message.from_user.id,'''Добро пожаловать, администратор!
В меню вы можете выбрать пункт который вас интересует.''',
        reply_markup = keyBoard_admin)
    elif message.text.split('/start ')[-1] in bouquets:
        bot.send_message(message.from_user.id, 'Выберите вариант доставки', reply_markup = keyBoard_delivery)
        buyer[tg_id] = []
        buyer[tg_id].append(message.text.split('/start ')[-1])
    else:
        bot.send_message(message.from_user.id, 'Вы не выбрали букет, который хотите купить. Вы можете посмотреть и выбрать букет на нашем канале @florico')

    with open('DB/buyer.pickle', 'wb') as f:
        pickle.dump(buyer,f)


@bot.message_handler(content_types = ['text'])
def get_text(message):
    global bufer_text
    global bufer_photo
    global bufer_sum
    global bufer_name

    tg_id = message.from_user.id

    with open('DB/buyer.pickle', 'rb') as f:
        buyer = pickle.load(f)

    if message.text == 'Добавить пост':
        os.mkdir(f'photos_{message.from_user.id}/')
        bufer_photo[tg_id] = []
        append_photo = bot.send_message(message.from_user.id, '''Добавьте фото для поста''', reply_markup = None)
    elif message.text == 'Закончить добавление':
        append_text = bot.send_message(message.from_user.id, '''Введите текст, который хотите разместить в посте''', reply_markup = None)
        bot.register_next_step_handler(append_text, append_text_accept)
    elif message.text == 'Изменить текст':
        bufer_text.pop(tg_id)
        bot.send_message(message.from_user.id, '''Отправьте текст заново''', reply_markup = None)
        bot.register_next_step_handler(message, append_text_accept)
    elif message.text == 'Текст введен верно':
        bot.send_message(message.from_user.id, '''Введите цену букета''')
        bot.register_next_step_handler(message,append_sum) 
    elif message.text == 'Посмотеть пост перед отправкой':
        bot.send_message(message.from_user.id, '''Ваш, пост будет выглядить так.
Хотите что-то изменить? Если нет, нажмите кнопку "Разместить пост"''')
        view_post(message)
    elif message.text == 'Разместить пост':
        bot.send_message(message.from_user.id, '''Ваш пост размещен!!!''', reply_markup = keyBoard_admin)
        send_post(message)
    elif message.text == 'Внести изменения':
        shutil.rmtree(f'photos_{message.from_user.id}/')
        bufer_photo.pop(tg_id)
        bufer_text.pop(tg_id)
        bufer_sum.pop(tg_id)
        bufer_name.pop(tg_id)
        os.mkdir(f'photos_{message.from_user.id}/')
        bufer_photo[tg_id] = []
        append_photo = bot.send_message(message.from_user.id, '''Добавьте фото для поста''', reply_markup = None)
    elif message.text == 'Самовывоз📦':
        bot.send_message(message.from_user.id, '''Вы сможте забрать свой букет по адресу:
г. Москва, ул. Нижняя, д.3️⃣ (м. Белорусская), цветочная мастерская 🌺Флорико🌺 
Наш номер телелефона +79151343030''', reply_markup = None)
        buyer[tg_id].append('Самовывоз')
        buyer[tg_id].append('г. Москва, ул. Нижняя, д.3️⃣ (м. Белорусская), цветочная мастерская 🌺Флорико🌺')
        print(buyer)
        with open('DB/buyer.pickle', 'wb') as f:
            pickle.dump(buyer,f)
        bot.send_message(message.from_user.id, '''Пожалуйста, оставьте свой номер телефона, чтобы мы могли связяться с вами📱
Напишите телефон в формате "+79151343030"''')
        bot.register_next_step_handler(message, append_phone)
    elif message.text == 'Доставка🚚':
        bot.send_message(message.from_user.id, '''Пожалуйста, укажите адрес доставки!!!
🚚Доставка по Москве бесплатно!''', reply_markup = None)
        buyer[tg_id].append('Доставка')
        bot.register_next_step_handler(message, delivery)
        with open('DB/buyer.pickle', 'wb') as f:
            pickle.dump(buyer,f)
    elif  message.text == 'Подтвердить и оплатить':
        buy_flower(message.from_user.id)
    elif  message.text == 'Изменить':
        bot.send_message(message.from_user.id, '''Давайте начнем заново! Выберите способ доставки''', reply_markup = keyBoard_delivery)
        buyer.pop(message.from_user.id)


if __name__ == '__main__':
    # app.run(host='127.0.0.1',
    #     port=7771)
     bot.polling(none_stop = True, interval = 0)