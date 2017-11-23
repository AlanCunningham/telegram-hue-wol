import logging
import ConfigParser

from telegram.ext import Updater, CommandHandler


class TelegramSam:

    config = ConfigParser.ConfigParser()

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s(): %(message)s')
        self.config.read('config.txt')

    def is_authorised_user(self, update):
        auth_user_id = int(self.config.get('telegram', 'auth_user'))
        current_user = update.message.from_user.id
        if auth_user_id == current_user:
            return True
        else:
            logging.critical('Unauthorised user request: %s' % current_user)
            return False

    # Bot commands
    def start(self, bot, update):
        if self.is_authorised_user(update):
            update.message.reply_text('Hi Alan!')

    def hello(self, bot, update):
        update.message.reply_text(
            'Hello {}'.format(update.message.from_user.first_name)
        )

    def start_updater(self):
        token_api = self.config.get('telegram', 'api_token')
        updater = Updater(token_api)
        updater.dispatcher.add_handler(CommandHandler('start', self.start))
        updater.dispatcher.add_handler(CommandHandler('hello', self.hello))
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    sam = TelegramSam()
    sam.start_updater()
