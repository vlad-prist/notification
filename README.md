# Сервис рассылки на Django (DRF)
Данный сервис является частью микросервисной архитектуры, которая обеспечивает работу большого проекта в части 
уведомлений пользорвателей на email или в telegram.


## Использование
Для работы с данным проектом:

* Установите Git и Docker

* Клонировать репозиторий. https://github.com/vlad-prist/notification.git

* В виртуальном окружении установите **requirements.txt** (пакет с зависимостями) с помощью команды:
```sh
$ pip install -r requirements.txt
```
celery -A config worker --loglevel=info -P eventlet