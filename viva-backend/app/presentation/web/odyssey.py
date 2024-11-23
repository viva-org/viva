import logging
import logging.handlers

import requests
from infrastructure.anki.VocabularyAgent import VocabularyAgent
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, \
    filters, CallbackContext, \
    CallbackQueryHandler

from application.video_review_processor import VideoReviewProcessor
from infrastructure.anki.anki_agent import AnkiAgent
from infrastructure.speech.eleven_labs_agent import ElevenLabsAgent
from infrastructure.text.chat_gpt_agent import ChatGptAgent


class MyBot:

    # documentation: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API
    # https://docs.python-telegram-bot.org/en/stable/telegram.video.html

    def __init__(self, token):
        self.application = ApplicationBuilder().token(token).build()
        self.setup_handlers()
        self.setup_logging()

    def setup_logging(self):
        # 创建一个日志器（Logger）
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)  # 设置日志级别为INFO

        # 创建一个到控制台的日志处理器（Handler）
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)

        # 创建一个到文件的日志处理器
        file_handler = logging.handlers.RotatingFileHandler(
            filename='bot.log',  # 日志文件路径
            maxBytes=1024 * 1024 * 5,  # 文件大小 5MB
            backupCount=2,  # 备份份数
            encoding='utf-8'  # 文件编码
        )
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)

        # 添加处理器到日志器
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    async def main_process(self, update: Update, context: CallbackContext) -> None:
        if update.message.text.startswith('s:'):
            vocabulary_agent = VocabularyAgent()
            all_synonyms = vocabulary_agent.find_synonyms(update.message.text.split(':')[1].strip())
            print(f"all_synonyms:{len(all_synonyms)}")
            my_words = vocabulary_agent.get_all_my_words()
            my_synonyms = all_synonyms.intersection(my_words)
            print(f"my_synonyms:{len(my_synonyms)}")
            if len(my_synonyms) <= 0:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="No synonyms in you vault.")
            else:
                keyboard = [
                    [InlineKeyboardButton("Synonym Contrast", callback_data='Synonym Contrast')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=str(my_synonyms), reply_markup=reply_markup)
        else:
            logging.info('context:', context)
            text = update.message.text
            logging.info('db.message:', update.message)
            # 逻辑处理
            self.text = update.message.text
            ElevenLabsAgent().generate_and_save_audio(self.text, 'Leo', 'eleven_monolingual_v1', 'audio/' + text[:20] + '.mp3')
            sentence = ChatGptAgent().generate_sentence_for_word(text)
            await context.bot.send_document(chat_id=update.effective_chat.id, document='audio/' + text[:20] + '.mp3')
            keyboard = [
                [InlineKeyboardButton("Add to Anki", callback_data='Add to Anki')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=sentence, reply_markup=reply_markup)

    async def anki_add_button(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        await query.answer()
        if query.data == 'Add to Anki':
            AnkiAgent().store_media_file_in_anki('audio/' +self.text[:20] + '.mp3',
                                                 open('audio/' + self.text[:20] + '.mp3', 'rb').read())
            front_value = query.message.text
            back_value = f"{self.text} <br> [sound:{self.text[:20] + '.mp3'}]"
            AnkiAgent().add_card_to_anki('odyssey', front_value, back_value)
            logging.info('anki added, text:', query.message.text)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="'" + self.text + "'" + " has added to Anki.")
        elif query.data == 'Synonym Contrast':
            await context.bot.send_message(chat_id=update.effective_chat.id, text="begin to contrast synonyms.")
            result = ChatGptAgent().discriminate_synonyms(query.message.text)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=result)

    def download_video(self, url, path_to_save):
        # 发送GET请求下载视频
        response = requests.get(url)
        # 确保请求成功
        if response.status_code == 200:
            # 将视频内容写入文件
            with open(path_to_save, 'wb') as file:
                file.write(response.content)
            print("视频成功下载到", path_to_save)
        else:
            print("下载视频失败，状态码：", response.status_code)

    async def video_process(self, update, context):
        # Inform the user that the vision has been received
        await update.message.reply_text('Video received! Processing...') # 注意要用阻塞的方式写
        # Access the vision file
        video_file = await update.message.video.get_file()  # 注意要用阻塞的方式写
        url = VideoReviewProcessor().execute(video_file.file_path)
        print('url:', url)
        # Respond to the user after processing is complete
        await context.bot.send_message(chat_id=update.effective_chat.id, text=" has .")

    async def cluster_cards(self, update: Update, context: CallbackContext) -> None:
        card_ids = AnkiAgent().get_cards_by_flag(1)
        cards_info =  AnkiAgent().get_cards_info(card_ids)

        words = []
        for card_info in cards_info:
            fields = card_info.get('fields', {})
            if 'Front' in fields and 'Back' in fields:
                front_full = card_info['fields'].get('Front', {}).get('value', 'Front field not found')
                back_full = card_info['fields'].get('Back', {}).get('value', 'Back field not found')
                start_index = 0
                end_index = back_full.find('&lt;br&gt;')
                chinese_sentence = front_full
                english_word = back_full[start_index:end_index].strip() if start_index < end_index else back_full
                words.append(chinese_sentence + " " + english_word)

        clustered_words = ChatGptAgent().cluster_words(words)
        if clustered_words:
            file_name = "../../clustered_words.txt"
            with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(str(words))
                    file.write(str(clustered_words))

            await context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_name, 'rb'))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No words clustered.")



    async def error_handler(self, update: Update, context: CallbackContext) -> None:
        logging.error(f"An error occurred: {context.error}")
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred, please try again later.")
            # restart
            self.run()
        except Exception as e:
            print(f"An error occurred while handling the error: {e}")
            # restart
            self.run()


    def setup_handlers(self):
        main_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.main_process)
        button_handler = CallbackQueryHandler(self.anki_add_button)
        cluster_handler = CommandHandler('cluster', self.cluster_cards)  # 注册 /cluster 命令的处理函数
        video_handler = MessageHandler(filters.AUDIO, self.video_process)  # 处理用户上传的


        self.application.add_handler(main_handler)
        self.application.add_handler(video_handler)  # 添加视频处理的 handler
        self.application.add_handler(button_handler)
        self.application.add_handler(cluster_handler)
        self.application.add_error_handler(self.error_handler)

    def run(self):
        self.application.run_polling()


if __name__ == '__main__':

    token = '6814680100:AAF8-zhTcO3BnagRv5rYFvS3qQiuxx6wYyY'
    my_bot = MyBot(token)
    my_bot.run()