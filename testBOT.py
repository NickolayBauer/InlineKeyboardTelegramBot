import config
import telebot

from telebot import types

bot = telebot.TeleBot(config.token)


def magic(one, two):
    d = one - two
    if d > 0:
        if (d % 2) == 1:
            return "@"+config.name2 + " победил"
        else:
            return "@"+config.name1 + " победил"
    elif d < 0:
        if (d % 2) == 0:
            return "@"+config.name2 +" победил"
        else:
            return "@"+config.name1 +" победил"
    else:
        return "ничья"



@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Нажми меня", callback_data="invite")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, "нажми, чтобы присоедениться", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "invite")
def callback_inline(call):
    config.name1 = config.name2 = config.id1 = config.id2 = config.player1 = config.player2 = ''
    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="камень", callback_data="0")
    callback_button2 = types.InlineKeyboardButton(text="ножницы", callback_data="1")
    callback_button3 = types.InlineKeyboardButton(text="бумага", callback_data="2")
    keyboard.add(callback_button1, callback_button2, callback_button3)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id, text="первый игрок выбирает",
                          reply_markup=keyboard)




@bot.callback_query_handler(func=lambda call: call.data in ["0","1","2"])
def callback_spisok(call):
    config.player1 = config.spisok[int(call.data)]
    config.name1 = call.from_user.username
    config.id1 = call.from_user.id


    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="камень", callback_data="3")
    callback_button2 = types.InlineKeyboardButton(text="ножницы", callback_data="4")
    callback_button3 = types.InlineKeyboardButton(text="бумага", callback_data="5")
    keyboard.add(callback_button1, callback_button2, callback_button3)
    bot.edit_message_text(chat_id=call.message.chat.id,
                         message_id=call.message.message_id, text = "второй игрок выбирает",
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ["3","4","5"])
def callback_spisok(call):
    config.player2 = config.spisok[int(call.data) - 3]
    config.name2 = call.from_user.username
    config.id2 = call.from_user.id
    if config.id1 != config.id2:
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="повторить", callback_data="invite")
        keyboard.add(callback_button1)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text=config.player1 + ' ' + config.player2 +
                                                                       '\n' + magic(config.spisok.index(config.player1),
                                                                                    config.spisok.index(
                                                                                        config.player2)),
                              reply_markup=keyboard)

    else:
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="ты играешь сам с собой")







if __name__ == '__main__':
    bot.polling(none_stop=True)
