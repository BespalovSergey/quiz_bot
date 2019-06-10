import os
import random
import logging
from dotenv import load_dotenv
from files_parser import get_data
from log_handler import MyLogsHandler
import telegram_dialog 
import vk_dialog


def main():

  logging.basicConfig(format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s ')
  logger = logging.getLogger('bot_logger')
  logger.setLevel(logging.INFO)
  logger.addHandler(MyLogsHandler(my_chat_id = os.environ['telegram_chat_id']))
  logger.info('Бот проверки ошибок викторины запущен')

  load_dotenv()
  questions  = get_data('questions')
  try:
    telebot = telegram_dialog.MyTelegram_bot(questions)
    telebot.telegram_bot()

    vkbot = vk_dialog.MyVkBot(questions)
    vkbot.vk_bot()
  except ConnectionError:
    logger.exception()  


if __name__ == "__main__":

  main()
