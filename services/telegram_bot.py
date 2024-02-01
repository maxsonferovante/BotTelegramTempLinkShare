import traceback

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
from telegram import Update

from env import TOKEN_TELEGRAM
from repositories.implementations.user_repository import UserRepository
from providers.temp_link_share_api import TempLinkShareAPI
from utils.generated_user_email import generated_user_email
from utils.generated_user_password import generated_user_password


class TelegramService:
    def __init__(self):
        self.app = ApplicationBuilder().token(TOKEN_TELEGRAM).build()
        self.userRepository = UserRepository()

    def run(self):
        self.up_handler()
        print('Starting Telegram bot')
        self.app.run_polling()

    def up_handler(self):
        self.app.add_handler(CommandHandler('start', self.welcome_command_handler))
        self.app.add_handler(MessageHandler(filters.Document.ALL, self.upload_command_handler))

    async def upload_command_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        file = await context.bot.get_file(update.message.document)
        await update.message.reply_text(f'File received, please wait a moment')
        await update.message.reply_text(f'File size: {file.file_size} bytes \n ')

    async def welcome_command_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_telegram = update.message.from_user
        try:
            check_user_exist = self.check_user_existence(user_telegram.id)
            if check_user_exist:
                await update.message.reply_text(f'Welcome back {user_telegram.first_name} {user_telegram.last_name}')
            else:
                self.create_user(user_telegram)
                await update.message.reply_text(f'Welcome {user_telegram.first_name} {user_telegram.last_name}')

        except Exception as e:
            print(e)
            await update.message.reply_text('Error creating user, please try again later.')

    def check_user_existence(self, chat_id: int) -> bool:
        user = self.userRepository.get_user_by_chat_id(chat_id)
        return user is not None

    def create_user(self, user_telegram):
        password = generated_user_password()
        email = generated_user_email(user_telegram.username, str(user_telegram.id))
        try:

            response_user_register = TempLinkShareAPI.user_register(email, password, user_telegram.first_name)
            if response_user_register:
                response_user_login = TempLinkShareAPI.user_login(email, password)
                self.userRepository.create_user(user_telegram.first_name,
                                                user_telegram.last_name,
                                                email, user_telegram.id,
                                                response_user_login['token'],
                                                password)
        except Exception as e:
            print(e)
            return traceback.print_exc()
