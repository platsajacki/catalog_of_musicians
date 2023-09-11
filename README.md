# COM. Catalog Of Musicians. (DRF)

Автор: [Vyacheslav Menyukhov](https://github.com/platsajacki) | menyukhov@bk.ru

[**Важно:**](#администратор)

## О проекте
Этот проект представляет собой API для каталога исполнителей, их альбомов и песен. Вы можете использовать Swagger для чтения документации и Postman для тестирования API.

## Технологии
- Django - веб-фреймворк для Python.
- Django REST framework (DRF) - расширение Django для создания RESTful API.
- SQLite - компактная встраиваемая СУБД.
- Docker - контейнеризатор приложений.

## Запуск проекта
Для запуска проекта выполните следующие шаги:

1. Установите необходимые зависимости, используя менеджер пакетов pip:
    ```bash
    git clone git@github.com:platsajacki/catalog_of_musicians.git
    ```

2. Перейдите в директорию проекта:
    ```bash
    cd catalog_of_musicians
    ```

3. Соберите Docker контейнер:
    ```bash
    docker build -t catalog_of_musicians .
    ```

4. Запустите проект с помощью следующей команды:
    ```bash
    docker run -p 8000:8000 catalog_of_musicians
    ```

## Администратор
**Профиль администратора создается автоматически с логином и паролем 'admin'.**

После успешного запуска проект будет доступен по адресу http://localhost:8000/. Вы также можете перейти на Swagger UI для ознакомления с документацией API по адресу http://localhost:8000/api/v1/swagger/.


## Использование Postman
Для тестирования API с помощью Postman импортируйте коллекцию Postman, предоставленную в этом проекте. В коллекции уже настроены запросы для создания, просмотра и обновления данных об исполнителях, альбомах и песнях.
