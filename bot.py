import telebot
import time


users = set()
helpingmessage = ''
TOKEN = '5929159617:AAG8Ty7oySL_i8lt09jnRmxG2niU8YeThfU'
bot = telebot.TeleBot(TOKEN)

def hmtimeswork(n):
  return (n*4)

def hmtimeshome(m):
  return (2*int((60//(int(m)))) + 1)


@bot.message_handler(commands=['start']) #Первое сообщение
def startuem(message):
  """
  Это сообщение отвечает за начала общения пользователя с ботом
  """
    global users
    kb = telebot.types.ReplyKeyboardMarkup(True, False)
    kb.row('/help', '/setting')
    if message.from_user.id in users:
        bot.send_message(
            message.chat.id,
            f'{message.from_user.first_name}, Выберите другую команду.',
            reply_markup=kb
        )
    else:
        users.add(message.from_user.id)
        bot.send_message(
            message.chat.id,
            f'Здравствуйте, {message.from_user.first_name}!',
            reply_markup=kb
        )


@bot.message_handler(commands=['help']) #Вспомогательное сообщение
def helpuem(message):
  """
  Это вспомогательное сообщение, чтобы объяснить, что пользователю требуется сделать, чтобы бот начал функционировать
  """
    global users
    if message.from_user.id in users:
        kb = telebot.types.ReplyKeyboardMarkup(True, False)
        kb.row('/setting')
        helpingmessage = f'{message.from_user.first_name}, чтобы бот начал свою работу, нажмите кнопку "setting". В дальнейшем вам придется выбрать несколько опций, чтобы бот действовал так, как вам было бы удобно.'
        bot.send_message(
            message.chat.id,
            helpingmessage,
            reply_markup=kb
        )


@bot.message_handler(commands=['setting']) #сообщение с настройкой бота
def setuem(message):
  """
  С помощью данной функции, бот дает пользователю варианты, чтобы второй выбрал свое местонахождение
  """
    global users
    if message.from_user.id in users:
        kb = telebot.types.ReplyKeyboardMarkup(True, False)
        kb.row('/work', '/home')
        helpingmessage = f'{message.from_user.full_name}, выберите, где вы сейчас находитесь, чтобы бот смог предложить удобные вам варианты промежутка между напоминаниями'
        bot.send_message(
            message.chat.id,
            helpingmessage,
            reply_markup=kb
        )

#Настройка бота относительно местонахождения
@bot.message_handler(commands=['work']) #Если пользователь на работе
def narabote(message):
  """
  На данном моменте бот просит пользователя ввести свой график работы (количество ежедневных часов работы)
  """
    global users
    if message.from_user.id in users:
        kb = telebot.types.ReplyKeyboardMarkup(True, False)
        kb.row('4', '6')
        kb.row('8', '10')
        kb.row('12')
        helpingmessage = 'Пожалуйста, когда вы начнете работать, выберите количество часов, которое вы отрабатываете каждый день. Если в предложенных вариантах нет подходящего вам, то напишите боту свой вариант.'
        bot.send_message(
            message.chat.id,
            helpingmessage,
            reply_markup=kb
        )
        @bot.message_handler(content_types=['text'])
        def inputmessage(message): #Считывается сообщение от пользователя
          """
          С помощью данной функции бот обрабатывает отправленное пользователем сообщение и использует данные из него
          """
            global b
            try: #Проверяется, правильный ли тип данных пользователь использовал в сообщении
                b = int(message.text)
                error = False
            except:
                error = True
            if not (error):
                stoppingmessage = True
                kb = telebot.types.ReplyKeyboardMarkup(True, False)
                kb.add('/settings')
                c = hmtimeswork(b)
                while stoppingmessage:
                    for i in range(0, c):
                        time.sleep(1)
                        helpingmessage = 'Выпрямите спину и разомнитесь.'
                        bot.send_message(
                            message.chat.id,
                            helpingmessage
                        )
                    stoppingmessage = False
                helpingmessage = f'{message.from_user.first_name}, возвращайтесь к нам завтра'
                bot.send_message(
                    message.chat.id,
                    helpingmessage,
                    reply_markup=kb
                )
                bot.register_next_step_handler(message, setuem)
            else:
                kb = telebot.types.ReplyKeyboardMarkup(True, False)
                kb.row('4', '6')
                kb.row('8', '10')
                kb.row('12')
                helpingmessage = 'Введите, пожалуйста, цифрами.'
                bot.send_message(
                    message.chat.id,
                    helpingmessage,
                    reply_markup=kb
                )
                bot.register_next_step_handler(message, inputmessage)


@bot.message_handler(commands=['home']) #Если пользователь находится дома
def doma(message):
  """
  На данном этапе бот просит пользователя ввести период, через который отправлять напоминание
  """
    global users
    if message.from_user.id in users:
        kb = telebot.types.ReplyKeyboardMarkup(True, False)
        kb.row('15', '20')
        kb.row('30', '60')
        helpingmessage = 'Пожалуйста, выберите период (в минутах), через который вам будет удобно получать уведомления. Если вам удобно исользовать свой период, то пожалуйста, напишите свой вариант боту'
        bot.send_message(
            message.chat.id,
            helpingmessage,
            reply_markup=kb
        )
        @bot.message_handler(content_types=['text'])
        def input_message(message): #Считывается содержание сообщения от пользователя
          """
          Данная функция обрабатывает сообщение пользователя и использует его для напоминания дома
          """
            global s
            try: #Проверяется, правильный ли тип данных использовал пользователь в сообщениях
                s = int(message.text)
                error = False
            except:
                error = True
            if not(error):
                stoppingmessage = True
                kb = telebot.types.ReplyKeyboardMarkup(True, False)
                kb.add('/home')
                t = hmtimeshome(s)
                while stoppingmessage:
                    for j in range(0, t):
                        time.sleep(60*(int(c)))
                        helpingmessage = 'Выпрямите спину и разомнитесь.'
                        bot.send_message(
                            message.chat.id,
                            helpingmessage
                        )
                    stoppingmessage = False
                helpingmessage = 'Хотите продолжить? Если да, нажмите "/home"'
                bot.send_message(
                    message.chat.id,
                    helpingmessage,
                    reply_markup=kb
                )
                bot.register_next_step_handler(message, doma)
            else:
                kb = telebot.types.ReplyKeyboardMarkup(True, False)
                kb.row('15', '20')
                kb.row('30', '60')
                helpingmessage = 'Введите цифрами, пожалуйста (или выберите один из предложенных вариантов).'
                bot.send_message(
                    message.chat.id,
                    helpingmessage,
                    reply_markup=kb
                )
                bot.register_next_step_handler(message, input_message)


bot.polling(none_stop=True)
