# Для работы бота следует установить:
### pip install pytelegrambotapi
### pip install Path
# Установка:
### Перед запуском следует изменить ключ бота в файле token_api.json
### Далее следует изменить путь сохранения для файлов пользователей в файле file_path.json
### После чего запуск производится через файлы start.bat или start.sh1
# Перезапуск бота:
### Для перезапуска бота следует использовать файлы restart.bat или restart.sh1
# Работа с БД:
### При первом обращение пользователя к боту создается база данных, далее используется. Если БД создана то последующие перезапуски бота не пересоздадут ее.
### !Если удалить базу данных, бот пересоздаст!
### Для работы с DB_Handler следует скопировать БД в папку с файлами DB_Handler.py ShowDB.bat ShowDB.ps1
# Документация:
### bot docs - https://github.com/eternnoir/pyTelegramBotAPI#types
### sqlbrowser - https://sqlitebrowser.org/
# Методы работы с ботом:
### @bot.message_handler(commands=['start']) - старт бота, реагирует на команду /start
### def name_method(message): - общий метод наследует message, может вызываться в любом месте как обработчик так и отдельный метод
### bot.register_next_step_handler(message, name_method) - регистрация следующего действия бота, требуется для логического перехода по обработчикам
### def start_data_base() - метод создания и проверки БД
### write_data_base() - метод записи данных от пользователя в БД
# Работа с очередью бота
### В конце кода предусмотрен обработчик очереди запросов к боту, в случае большой нагрузки следует изменить параметр interval на 2-5, задержка ответа пользователю увеличится
