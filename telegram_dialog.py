from telegram.ext import Updater ,CommandHandler, MessageHandler, Filters , ConversationHandler ,RegexHandler
from telegram import ReplyKeyboardMarkup
import os
import random
from files_parser import get_data
import redis




class MyTelegram_bot():

  NEW_QUESTION ,MY_RESULT  = range(2)

  def __init__(self ,questions  ):
    self.questions = questions
    self.keys = list(questions.keys())
    self.r = redis.Redis(host = os.environ['redis_adress'] ,
    password = os.environ['redis_password'], port = os.environ['redis_port']  ,decode_responses=True, db = 0
    )

    
  def get_keyboard(self ,buttons= [['Новый вопрос','Сдаться'],['Мой счёт']]):
    return ReplyKeyboardMarkup(buttons)


  def get_question_index(self , chat_id):
    index = -1
    redis_data = self.r.get(chat_id)
    if redis_data:
      index = self.keys.index(redis_data)
    return index 


  def  handle_new_question_request(self,bot ,update):
    index = self.get_question_index(update.message.chat_id)
    try :
      self.r.set(update.message.chat_id , self.keys[index +1])
      result =  self.keys[index+1]
    except IndexError:
      result = self.keys[0]   
    update.message.reply_text(result , reply_markup = self.get_keyboard())  


  def  handle_solution_attempt(self, bot, update):
    index = self.get_question_index(update.message.chat_id)
    text = update.message.text
    result = ''
    if index > -1:

      text = text.lower()  
      right_answer = self.questions[self.keys[index]].lower()
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
    result = self.questions[self.keys[index]]
    update.message.reply_text(result, reply_markup = self.get_keyboard())
    self.handle_new_question_request(bot ,update)


  def my_score(self, bot ,update):
    result = 'Статистика не ведётс'
    update.message.reply_text(result, reply_markup = self.get_keyboard())

    
  def start(self,bot ,update):
    bot.send_message(chat_id = update.message.chat_id,
    text = 'Здравствуйте , я  бот викторины' ,reply_markup = self.get_keyboard())

  
  def telegram_bot(self):
  
    updater = Updater(os.environ['bot_quiz_telegram_token'])
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
      entry_points = [CommandHandler('start', self.start),
                      RegexHandler('Новый вопрос' , self.handle_new_question_request),
                      RegexHandler('Сдаться' , self.handle_surrend),
                      RegexHandler('Мой счёт' , self.my_score),
                      MessageHandler(Filters.text,self. handle_solution_attempt)
                      
                      
                     ],

      states = {},
      fallbacks=[]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()   


