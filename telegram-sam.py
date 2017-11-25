import logging
import ConfigParser

from telegram.ext import Updater, CommandHandler
from wakeonlan import wol

config = ConfigParser.ConfigParser()


def init():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s(): %(message)s')
    config.read('config.txt')
    start_updater()


def check_authorised_user(func):
    def auth_check(bot, update):
        auth_user_id = int(config.get('telegram', 'auth_user'))
        current_user = update.message.from_user.id
        if auth_user_id == current_user:
            func(bot, update)
        else:
            bot.send_message(
                chat_id=auth_user_id,
                text='Unauthorised user request: %s %s | %s' %
                (update.message.from_user.first_name,
                    update.message.from_user.last_name,
                    update.message.text
                )
            )
            return False
    return auth_check


# Bot commands
@check_authorised_user
def start(bot, update):
    update.message.reply_text('Hi Alan!')


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name)
    )


@check_authorised_user
def wake_computer(bot, update):
    wol.send_magic_packet(config.get('computer', 'mac_address'))
    update.message.reply_text('Sending wake on lan request')


def start_updater():
    api_token = config.get('telegram', 'api_token')
    updater = Updater(api_token)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('computer', wake_computer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    init()
