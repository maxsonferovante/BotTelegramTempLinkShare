import traceback
from typing import BinaryIO
import io

import telegram.error
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
        self.app.add_handler(CommandHandler('refresh', self.refresh_command_handler))
        self.app.add_handler(MessageHandler(filters.Document.ALL, self.upload_command_handler))

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

        email = generated_user_email(user_telegram.username, user_telegram.id)
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

    async def refresh_command_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        try:
            check_user_exist = self.check_user_existence(update.message.from_user.id)
            if check_user_exist:

                user_telegram = self.userRepository.get_user_by_chat_id(update.message.from_user.id)

                response_user_login = TempLinkShareAPI.refresh_token(user_telegram.token)

                self.userRepository.update_user_token(user_telegram, response_user_login['token'])

                await update.message.reply_text(f'Session refreshed with success!')
            else:
                await update.message.reply_text(f'User not found, please send /start command and try again.')

        except Exception as e:
            print(e)
            await update.message.reply_text('Error refreshing session, please try again later')

    async def upload_command_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            file = await update.message.effective_attachment.get_file()

            await update.message.reply_text(f'File received, please wait a moment')
            file_out: BinaryIO = io.BytesIO()
            await file.download_to_memory(out=file_out)

            if not self.check_user_existence(update.message.from_user.id):
                await update.message.reply_text(f'User not found, please send /start command and try again.')
            else:
                user_telegram = self.userRepository.get_user_by_chat_id(update.message.from_user.id)
                try:
                    response_upload = TempLinkShareAPI.upload_file(file_out, user_telegram.token)
                    await update.message.reply_text(
                        f'<b>File saved with success!</b>\n'
                         f'You can access it through the following link:\n'
                         f'<a href="{response_upload["responseUploaded"]["url"]}">File Link</a>.\n'
                         f'This link will be available until <i>{response_upload["experationData"]}</i>.\n',
                            parse_mode='HTML')

                except Exception as e:
                    if 'Invalid token' in str(e):
                        await update.message.reply_text('Session expired, please send /refresh command and try again.')
                    else:
                        print('(TempLinkShareAPI.upload_file):', e)
                        await update.message.reply_text('Error sending file to please try again later')

        except telegram.error.BadRequest as e:
            if 'File is too big' in str(e):
                await update.message.reply_text('File is too big, please send a file less than 20MB')
            else:
                await update.message.reply_text('Error sending file, please try again later')