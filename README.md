# Foodgram - Соцсеть для обмена вкусняшками (рецептами)
![Project status](https://github.com/PinCatS/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Проект курса "Python-разработчик плюс" от Яндекс.Практикум в котором необходимо было разработать backend для соцсети Foodgram, где люди могут создавать рецепты, подписываться на пользователей и их рецепты, добавлять рецепты в корзину и скачивать список ингредиентов для покупки. 

## Технологии
* Django Rest Framework
* Django Authtoken + Djoser
* Python 3.10.7
* PostgreSql
* Git
* Docker
* GitHub Actions

## Доступ к проекту
* Проект доступен по адресу `http://130.193.41.249/`
* Админка доступна по адресу `http://130.193.41.249/admin/`
* В админку можно зайти через администратора: `admin@foodgram.ru`, пароль `change_me`
* Документацию по backend API можно посмотреть тут: `http://130.193.41.249/api/docs/`
## CI/CD
Для проекта настроен GitHub Action workflow.
При пуше в master, проект проверяется на соответствие PEP8, собирается образ `pincats/foodgram-backend: latest` backend и отправляется на DockerHub. Затем проект деплоится в Yandex.Cloud. При успешном деплое, приходит сообщение в телеграм.

## Авторы
Сергей Ли
