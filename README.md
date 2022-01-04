# Босc службы поддержки
Чат-боты службы поддержки в `Telegram` и `ВКонтакте` на основе `DialogFlow`.
Автоматические ответы на заданные темы, например:
- есть ли вакансии?
- как удалить учетную запись?
- почему меня "забанили"?
- приветствие?
и другие

Возможность подключить любые темы и ответы на них использую как ручную настройку в `DialogFlow`, 
так и загрузку из подготовленного файла `json` (Вопросы-Ответы).
Возможность присылать "неизвестные" запросы администратору систему напрямую в `Telegram`

## Пример работы бота

1. Чат-бот в сообществе ВКонтакте. Можно попробовать [тут](https://vk.com/im?sel=-194825636).

![Чат-бот в сообществе ВКонтакте](https://github.com/kruser66/support-bot/blob/main/example/vk_bot_example.gif)

2. Чат-бот в Телеграм. Можно попробовать [тут](https://t.me/kruser_support_bot).

![Чат-бот в Телеграм](https://github.com/kruser66/support-bot/blob/main/example/tg_bot_example.gif)

# Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```
1. Для работы необходимо зарегистрироваться в [Google Cloud Platform](https://cloud.google.com/) -> `Get started for free`
2. Создать новый проект (New project). Для чат-бота нужен будет `project_id`
3. Создать `Service Account` и получить для него ключи в формате `json` скачать в папку своего проекта
4. Зарегистрироваться в [DialogFlow](https://dialogflow.cloud.google.com/)
5. Создать нового агента (Creat new agent) и указать для него `project_id`, полученный в Google Cloud
6. Создать New Intent - объект отвечающий за ответы на вопросы определнной тематики. Содержит тренировочные фразы и ответы на них. 


# Пример использования

## Для работы чат-бота понадобятся следующие переменные окружения:
- Токен для бота Telegram

```
TG_BOT_TOKEN='YOUR_TELEGRAM_BOT_TOKEN'
```

- ID чата в Телеграмм Администратора для получения "некорректных" запросов

```
TG_CHAT_ID='TELEGRAM_ADMIN_CHAT_ID'
```

- ID проекта Google, полученный в п.2

```
GOOGLE_CLOUD_PROJECT_ID='project_id'
```

- Путь до `json` ключа `GoogleCloud` для вашего проекта `project_id` 

```
GOOGLE_APPLICATION_CREDENTIALS='LINK_TO_YOUR_JSON_KEY'
```

- Для чат-бота в ВКонтакте понадобится

```
VK_GROUP_TOKEN='YOUR_VK_GROUP_TOKEN'
```

Права доступа: сообщения сообщества, фотографии, стена


## Запуск модуля чат-бота Telegram

```
python tg_support_bot.py
```

## Запуск модуля чат-бота ВКонтакте

```
python vk_support_bot.py
```

## Загрузка `intents` в `DialogFlow`

Пример загрузки тренировочных фраз и ответов из файла `questions.json`
```
python intents.py
```

# Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](dvmn.org).
