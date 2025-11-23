import logging  # Импортируем модуль для логирования событий в приложении
import asyncio # Для реализации задержки при опросе ассистента

from openai import OpenAI  # Импортируем класс OpenAI для работы с API OpenAI
from telegram import Update  # Импортируем класс Update для обработки обновлений Telegram
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes  # Импортируем компоненты из telegram.ext для создания и управления ботом

from src import OPENAI_API_KEY, ASSISTANT_ID, TELEGRAM_TOKEN  # Импортируем необходимые ключи и токены из локального модуля src

# --- Инициализация клиентов ---
client = OpenAI(api_key=OPENAI_API_KEY)  # Создаём клиент OpenAI, передавая API-ключ

# --- Логирование ---
logging.basicConfig(level=logging.INFO)  # Устанавливаем базовый уровень логирования — INFO
logger = logging.getLogger(__name__)  # Получаем объект логгера для текущего модуля

# Для каждого пользователя храним:
user_data = {}  # user_id: { "thread_id": str, "last_message_id": str | None }

# --- Приветственное сообщение ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Обработчик команды /start — отправляет приветственное сообщение
    await update.message.reply_text(
        "Привет! Я бот- ассистент инвестора.\n"
        "Умею генерировать необычные идей проектов для инвестиций в сфере ИТ, рассчитанные на реализацию одним профессиональным ИТ-специалистом\n"
        "Напишии тему или бюджет - и я придумаю три идеи с разной степенью риска."
    )
    
# --- Основная логика ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text  # Получаем текст сообщения пользователя
    user_id = update.message.from_user.id  # Получаем идентификатор пользователя

    status_msg = await update.message.reply_text("Обрабатываю запрос...")  # Сообщаем пользователю о процессе обработки

    try:
        # --- Инициализация данных пользователя ---
        if user_id not in user_data:
            user_data[user_id] = {
                "thread_id": client.beta.threads.create().id,
                "last_message_id": None,
            }

        thread_id = user_data[user_id]["thread_id"] # поток для пользователя
        last_message_id = user_data[user_id]["last_message_id"] # последнее полученное сообщение пользователя

        # Отправляем сообщение пользователя в созданный поток OpenAI
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message
        )

        # Запускаем ассистента для обработки потока
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )

        # Ожидаем завершения обработки (пока статус - в очереди или выполняется)
        while run.status in ("queued", "in_progress"):
            await asyncio.sleep(0.5)  # нормальная задержка
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

        # Получаем список всех новых сообщений в потоке (будет отсортирован от старыx к новым)
        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            order="asc",
            after=last_message_id
        ).data

        # Извлекаем новые ответы ассистента из сообщений потока
        new_responses = []
        print("new messages:")
        for msg in messages:
            print(msg.role, msg.id)
            if msg.role == "assistant":
                text = msg.content[0].text.value
                new_responses.append(text)

        # Обновляем last_message_id
        if messages:
            user_data[user_id]["last_message_id"] = messages[-1].id

        # Собираем все новые ответы ассистента в одну строку, если они есть, иначе выводим сообщение об отсутствии ответа
        if new_responses:
            response = "\n".join(new_responses)
        else:
            response = "Ассистент ничего не ответил."
        await status_msg.edit_text(response)  # Обновляем статусное сообщение на ответ ассистента

    except Exception as e:
        logger.error(e)  # Логируем ошибку
        await update.message.reply_text("Ошибка при обработке запроса. Попробуйте позже.")  # Отправляем сообщение об ошибке пользователю

# --- Запуск бота ---
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()  # Инициализируем приложение Telegram бота с токеном

    # Добавляем обработчик команды /start
    app.add_handler(CommandHandler("start", start))  
    # Добавляем обработчик всех текстовых сообщений, кроме команд
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  

    print("✅ Бот запущен!")  # Выводим сообщение о запуске бота в консоль
    app.run_polling()  # Запускаем бесконечный цикл ожидания событий (polling)

if __name__ == "__main__":
    main()  # Запускаем функцию main, если скрипт исполняется как основной
