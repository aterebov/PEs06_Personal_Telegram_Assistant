# Урок PEs06. Проект: Персональный помощник через API

## Описание

Telegram-бот - персональный помощник - генератор необычных идей проектов для инвестиций в сфере ИТ, рассчитанных на реализацию одним профессиональным ИТ-специалистом.  
Бот интегрирован с OpenAIAssistant.
Подготовлена интеграция бота напрямую с LLM-моделями GigaChat (с использоваением библиотеки LangChain) и OpenAI.

***

## Дополнительная информация
1. Для запуска проекта потребовалось обновить python-telegram-bot до последней версии
pip install --upgrade python-telegram-bot

2. Рабочее окружение зафиксировано в файле requirements.txt командой:
pip freeze > requirements.txt

Воспроизвести его можно будет командой:
pip install -r requirements.txt

3. Для выполнения запроса к OpenAI при запуске на локальном компьютере может потребоватья VPN

***

## Структура проекта

- **OpenAI Assistant:**  
  Код интеграции: [`main_open_ai.py`](https://github.com/ZerocoderUniversity/AI-course-prompt-engineering-3.0/blob/7e7dfebdb0a5d213e4e61f56835994f2fd079e04/01_Project_Personal%20API-assistant/main_open_ai.py)

- **LLM GigaChat с библиотекой LangChain:**  
  Код интеграции: [`main_giga.py`](https://github.com/ZerocoderUniversity/AI-course-prompt-engineering-3.0/blob/7e7dfebdb0a5d213e4e61f56835994f2fd079e04/01_Project_Personal%20API-assistant/main_giga.py)

- **LLM OpenAI:**  
  Код интеграции: [`main_lang.py`](https://github.com/ZerocoderUniversity/AI-course-prompt-engineering-3.0/blob/7e7dfebdb0a5d213e4e61f56835994f2fd079e04/01_Project_Personal%20API-assistant/main_lang.py)

- **Загрузка ключей и паролей (.env):**  
  Автоматическая загрузка: [`src.py`](https://github.com/ZerocoderUniversity/AI-course-prompt-engineering-3.0/blob/e16af58d6c1ee5d21b2880a2402bb58a25721875/01_Project_Personal%20API-assistant/src.py)

***

## Важно!

Секреты (API Keys, passwords) бот получает из переменных окружения, которые инициализируются при старте бота из текстового файла `.env`.

**Формат строки файла `.env`:**

```
КЛЮЧ=значение
```

**Пример файла `.env`:**

```
OPENAI_API_KEY=sk-xxx-xxx
ASSISTANT_ID=asst-xxx-xxx
TELEGRAM_TOKEN=123456789:AbcDefGHIjklMNOpQRstUvWxyXz
GIGACHAT_CREDENTIALS=my_gigachat_service_token
LANGFUSE_SECRET_KEY=my_langfuse_secret
LANGFUSE_PUBLIC_KEY=my_langfuse_public
LANGFUSE_HOST=https://my.langfuse.server
```

- Слева — имя (ключ) переменной  
- Справа — её значение

**Рекомендация:**  
Добавьте `.env` в `.gitignore`, чтобы секреты не попадали в публичный репозиторий.
