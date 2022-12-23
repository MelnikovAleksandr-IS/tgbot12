import telebot
import time


users = set()
helpingmessage = ''
TOKEN = '5929159617:AAG8Ty7oySL_i8lt09jnRmxG2niU8YeThfU'
bot = telebot.TeleBot(TOKEN)

def hmtimeswork(n):
  """
  Результатом этой функции является приведение введеного пользователем количество часов работы
  в количество раз, сколько бот ему будет высылать напоминание
  n - введеное пользователем количество часов
  """
  return (n*4)

def hmtimeshome(m):
  """
  Результатом этой функции является приведение введеного пользователем периода, через который пользователь хочет получать напоминания
  в количество раз, сколько бот ему будет высылать напоминание
  m - введеный пользователем период напоминания
  """
  return (2*int((60//(int(m)))) + 1)


@bot.message_handler(commands=['start']) #Первое сообщение
def startuem(message):
  """
  Результатом этой функции является отправка сообщения с приветствием пользователя и создание клавиатуры со вспомогательными кнопками
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
  Результатом этой функции является отправка сообщения пользователю с объяснениями, как пользователю настроить бота
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
  Результатом этой функции является отправка сообщения пользователю о том, чтобы он сообщил о своем местоположении,
  чтобы бот смог самостоятельно подобрать программу по напоминаниям, и появление новой клавиатуры
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
  Результатом этой функции является отправка пользователю сообщения с просьбой уточнить количество часов, сколько по графику он отрабатывает за день
  и появления клавиатуры с некоторыми вариантами того самого количества часов
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
          Результатом этой функции является периодическое напоминание пользователю поправить осанку и проверка правильности введенного сообщения
          и возвращение к функции настройки после окончания рабочего дня
          (если сообщение нельзя перевести в тип integer, то бот попросит пользователя ввести сообщение с корректными данными)
          b берет значение из message.text и преобразует его в целое число
          time.sleep() используется для того, чтобы создать перерыв между сообщениями с напоминанием
          c - значение, которое получается после обработки переменной b с помощью функции hmtimeswork
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
                        time.sleep(60*15)
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
  Результатом этой функции является отправка пользователю сообщения с просьбой, чтобы пользователь отправил период,
  через который он хотел бы получать уведомления напоминания от бота, и появление клавиатуры с вариантами таких периодов
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
          Результатом этой функции является периодическое напоминание пользователю поправить осанку и проверка правильности введенного сообщения
          (если сообщение нельзя перевести в тип integer, то бот попросит пользователя ввести сообщение с корректными данными)
          и возвращение в меню настройки бота или к меню '/home'
          s берет значение из message.text и преобразует его в целое число
          time.sleep() используется для того, чтобы создать перерыв между сообщениями с напоминанием
          t - значение, которое получается после обработки переменной b с помощью функции hmtimeswork
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
                kb.row('/home', '/settings')
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
                helpingmessage = 'Хотите продолжить? Если да, нажмите "/home" или "/settings"'
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
""" 
Бот постоянно спрашивает сервера телеграмм на наличие новых сообщений
"""
