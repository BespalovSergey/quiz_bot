import os
import logging
from dotenv import load_dotenv
from files_parser import get_questions
from log_handler import MyLogsHandler
import telegram_dialog 
import vk_dialog


def main():

  logging.basicConfig(format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s ')
  logger = logging.getLogger('bot_logger')
  logger.setLevel(logging.INFO)
  logger.addHandler(MyLogsHandler(my_chat_id = os.environ['QUIZ_TELEGRAMM_CHAT_ID']))
  logger.info('Бот проверки ошибок викторины запущен')

  load_dotenv()
  questions  = get_questions('questions')
  try:
    telebot = telegram_dialog.MyTelegram_bot(questions)
    telebot.run_telegram_bot()

    vkbot = vk_dialog.MyVkBot(questions)
    vkbot.run_vk_bot()
  except ConnectionError:
    logger.exception()  


if __name__ == "__main__":

  main()

