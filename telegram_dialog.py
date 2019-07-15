from telegram.ext import Updater ,CommandHandler, MessageHandler, Filters , ConversationHandler ,RegexHandler
from telegram import ReplyKeyboardMarkup
import os
import random
from files_parser import get_questions
import redis




class MyTelegram_bot():

  NEW_QUESTION ,MY_RESULT  = range(2)

  def __init__(self ,questions  ):
    self.questions = questions
    
    self.r = redis.Redis(host = os.environ['QUIZ_REDIS_ADDRESS'] ,
     password = os.environ['QUIZ_REDIS_PASSWORD'],
     port = os.environ['QUIZ_REDIS_PORT'],
     decode_responses=True, db = 0
    )

    
  def get_keyboard(self ,buttons= [['Новый вопрос','Сдаться'],['Мой счёт']]):
    return ReplyKeyboardMarkup(buttons)


  def get_question_index(self , chat_id):
    index = -1
    redis_key = 'tg_{}'.format(chat_id)
    redis_data = self.r.get(redis_key)

    if redis_data:
      index = redis_data
    return int(index )


  def  handle_new_question_request(self,bot ,update):
    index = self.get_question_index(update.message.chat_id)
    redis_key = 'tg_{}'.format(update.message.chat_id)
    try :
      self.r.set(redis_key , index+1)
      result =  self.questions[index+1][0]
    except IndexError:
      self.r.set(redis_key , 0)
      result = self.questions[0][0]   

    update.message.reply_text(result , reply_markup = self.get_keyboard())  


  def  handle_solution_attempt(self, bot, update):
    index = self.get_question_index(update.message.chat_id)
    text = update.message.text
    result = ''
    if index > -1:

      text = text.lower()  
      right_answer = self.questions[index][1].lower()
      flag = ''

      if '(' in right_answer:
        right_answer = right_answer[0:right_answer.find('(')]
      elif '.' in  right_answer:
        right_answer = right_answer[0:right_answer.find('.')]
        
      if text == right_answer:
        result = 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»'
      else:
        result =  'Неправильно... Попробуешь ещё раз?'

    else:
      result =  'Вопрос ещё не задан'
    update.message.reply_text(result , reply_markup = self.get_keyboard())  


  def handle_surrend(self, bot, update):
    result = ''
    index = self.get_question_index(update.message.chat_id)

    if index == -1:
      result ='Рано сдаётесь , вопрос ещё не задан !'

    result = self.questions[index][1]
    update.message.reply_text(result, reply_markup = self.get_keyboard())
    self.handle_new_question_request(bot ,update)


  def get_my_score(self, bot ,update):
    result = 'Статистика не ведётся'
    update.message.reply_text(result, reply_markup = self.get_keyboard())

    
  def start(self,bot ,update):
    bot.send_message(chat_id = update.message.chat_id,
    text = 'Здравствуйте , я  бот викторины' ,reply_markup = self.get_keyboard())

  
  def run_telegram_bot(self):
  
    updater = Updater(os.environ['QUIZ_TELEGRAMM_TOKEN'])
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
      entry_points = [CommandHandler('start', self.start),
                      RegexHandler('Новый вопрос' , self.handle_new_question_request),
                      RegexHandler('Сдаться' , self.handle_surrend),
                      RegexHandler('Мой счёт' , self.get_my_score),
                      MessageHandler(Filters.text,self. handle_solution_attempt)
                      
                      
                     ],

      states = {},
      fallbacks=[]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()   
