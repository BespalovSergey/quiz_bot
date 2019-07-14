import os
import random
import redis
import vk_api
from vk_api.longpoll import VkLongPoll ,VkEventType
from vk_api.keyboard import VkKeyboard ,VkKeyboardColor


class MyVkBot():
  
  def __init__(self, questions):
    self.questions = questions
   
    self.r = redis.Redis(host= os.environ['redis_adress'],
              password = os.environ['redis_password'],
              port = os.environ['redis_port'],
              decode_responses = True, db = 0)


  def get_keyboard(self):
    keyboard = VkKeyboard(one_time = True)
    keyboard.add_button('Новый вопрос', color = VkKeyboardColor.DEFAULT)
    keyboard.add_button('Сдаться', color = VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color = VkKeyboardColor.DEFAULT)
    return keyboard.get_keyboard()

    
  def get_question_index(self , chat_id):
    index = -1
    redis_key = 'vk_{}'.format(chat_id)
    redis_data = self.r.get(redis_key)
    if redis_data:
      index = redis_data
    return int(index)   


  def new_question(self , user_id ,index):  
    redis_key = 'vk_{}'.format(user_id)
    try :
      self.r.set(redis_key , index +1)
      return self.questions[index+1][0]
        
    except IndexError:
      self.r.set(redis_key , 0)
      return self.questions[0][0] 


  def answer_bot(self, event): 
    text = event.text
    index = self.get_question_index(event.user_id)
  
    if text == 'Новый вопрос':
      return self.new_question(event.user_id , index)

    elif text ==  'Сдаться' :
      if index == -1:
        return 'Рано сдаётесь , вопрос ещё не задан !'
      return self.questions[index][1]

    elif text == 'Мой счёт':
      return 'Статистика не ведётся' 

    else:
      if index > -1:
        text = text.lower()  
        right_answer = self.questions[index][1].lower()
        
        if '(' in right_answer:
          right_answer = right_answer[0:right_answer.find('(')]
        elif '.' in  right_answer:
          right_answer = right_answer[0:right_answer.find('.')]
        
        if text == right_answer:
          return 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»'
        else:
          return 'Неправильно... Попробуешь ещё раз?'

      else:
        return 'Вопрос ещё не задан'

  
  def echo(self ,event , api):
    keyboard = self.get_keyboard()
    api.messages.send(user_id  = event.user_id,
                    message = self.answer_bot(event),
                    random_id = random.randint(1,1000),
                    keyboard = keyboard)

    if event.text == 'Сдаться':
      event.text = 'Новый вопрос'
      api.messages.send(user_id  = event.user_id,
                    message = self.answer_bot(event),
                    random_id = random.randint(1,1000),
                    keyboard = keyboard)


  def vk_bot(self):
    vk_session = vk_api.VkApi(token = os.environ['vk_token'])
    vk_ap = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
      if event.type == VkEventType.MESSAGE_NEW  and event.to_me:
        self.echo(event ,vk_ap)     
      
  
