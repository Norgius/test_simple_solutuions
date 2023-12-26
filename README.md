# Test Stripe Payment

Все настройки и секреты прописываем в файле `.env`, который нужно создать в корневой директории проекта.

Для запуска проекта вам потребуется зарегистрироваться на [stripe.com](https://stripe.com/) и получить там `STRIPE_PUBLIC_KEY` и `STRIPE_SECRET_KEY`.

Также для подключения `webhook` нужно будет будет добавить `endpoint` на сайте, если подключаете локально, то воспользуйтесь [ссылкой](https://stripe.com/docs/stripe-cli#install), после подключения получите `STRIPE_ENDPOINT_SECRET`.

В случае подключения на сервере просто создайте `webhook` в соответствующем разделе [сайта](https://dashboard.stripe.com/webhooks/) и также получите оттуда необходимый секрет.

Для подключения к `PostgreSQL` укажите следующие настройки:
 * POSTGRES_USER
 * POSTGRES_PASSWORD
 * POSTGRES_DB

Секреты `Django`:
 * SECRET_KEY
 * ALLOWED_HOSTS
 * POSTGRES_DSN (пример: `postgres://postgres:postgres@db:5432/postgres`)
 * YOUR_DOMAIN (http://127.0.0.1:8000 или http://example.com)
 * DEBUG


## _Development_

Скачайте и соберите докер-образы с помощью Docker Сompose:
```sh
$ docker compose pull --ignore-buildable
$ docker compose build
```

Запустите докер-контейнеры и не выключайте:
```sh
$ docker compose up
```

Примените миграции:
```sh
$ docker compose run --rm django python manage.py migrate
```

И создайте нового суперпользователя:
```sh
$ docker compose run --rm django python manage.py createsuperuser
```

## _Production_

Находясь в корневой директории проекта создайте каталог `static`:
```sh
mkdir static
```

Перейдите в директорию `docker_production/`. Дополните `nginx.conf` вашим `ip` или `доменом`:
```sh
server_name ***********;
```

Оставаясь в этой же директории повторите те же шаги, что указаны в _`Development`_.
