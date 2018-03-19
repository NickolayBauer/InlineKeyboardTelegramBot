import config
import telebot

from telebot import types

bot = telebot.TeleBot(config.token)

def magic(one, two):
    d = one-two
    if d > 0:
        if (d % 2) == 1:
            return "второй игрок победил"
        else:
            return "первый игрок победил"
    elif d < 0:
        if (d % 2) == 0:
            return "второй игрок победил"
        else:
            return "первый игрок победил"
    else:
        return "ничья"

@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Нажми меня", callback_data="invite")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, "нажми, чтобы присоедениться", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print(type(call.data))
    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="камень", callback_data="0")
    callback_button2 = types.InlineKeyboardButton(text="ножницы", callback_data="1")
    callback_button3 = types.InlineKeyboardButton(text="бумага", callback_data="2")
    keyboard.add(callback_button1, callback_button2,callback_button3)
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "invite":
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, text="сейчас появилась "
                                                                           "новая клавиатура, я догадывался,"
                                                                           "как сделать ещё дофига времени",
                                  reply_markup = keyboard)

        elif call.data in ["0","1","2"] and config.player1 == '':
            config.player1 = config.spisok[int(call.data)]
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, text="ваш противник выбрал, ваша очередь",
                                  reply_markup = keyboard)

        elif call.data in ["0", "1", "2"] and config.player1 != '':
            config.player2 = config.spisok[int(call.data)]

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, text=str(call.from_user) + config.player1 +' '+ config.player2 +
                                  '\n' +magic(config.spisok.index(config.player1),config.spisok.index(config.player2)))
            config.player1 =config.player2 = ''

if __name__ == '__main__':
    bot.polling(none_stop=True)