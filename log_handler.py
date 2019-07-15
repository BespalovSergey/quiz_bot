import logging
import telegram
import os


class MyLogsHandler(logging.Handler):
    def __init__(self,my_chat_id):
        super().__init__()
        self.error_bot = telegram.Bot(token= os.environ['QUIZ_BOT_ERROR_TOKEN'])
        self.my_chat_id = my_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        bot_down = 'Бот telegtam_dialog упал с ошибкой \n'
        error_message = '{}{}'.format(bot_down, log_entry)

        if log_entry == 'Бот проверки ошибок викторины запущен':
            error_message = 'Бот проверки ошибок викторины запущен'

        self.error_bot.send_message(chat_id=self.my_chat_id, text=error_message)
