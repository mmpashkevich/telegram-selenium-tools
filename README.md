# mihkevich/telegram-selenium-tools

## Description


This project is my mini toolbox, used telegram-bot how interface for anything of functional, such as:
-  receive weather from
my lovely site foreca.ru in screenshors form; 
- send link to audio track from service of yandex music and recieve mp3 file
- speak with AI on chat, uses open source technologies


On this moment realized only one mini-feature - receive weather  by my city Rostov-on-Don on anything message to bot. Thar very simple design. Each minute worker of selenium_service saving picture into json file, which request telegram_service throught REST API, when user send anything message to bot. 

> I`m have in future plan of idea realization of schema with Celery, Redis and MongoDB for abilities:
> - provide weather from popular cities
> - request weather by periodes from database
> - bot sending to chat each day weather according to the settings (city, requency, text of analize)

## Instalation and run

That project dockerized, therefore it simple of manage, if operation of system have installed docker and docker-compose.
Project have three entripoint by two microservices.

1) telegram_bot run from telegram_bot.main.py for listening messages from users, request by REST API image on format of base64 and answer of picture to user on message 
2) api.py which run uvicorn for FastApi. It use selenium_service for receive image.
3) selenium_service, which run worker. Worker run script for obtaining screenshot every minute and save it on disk in json-file

### First us build it, run command
```sh 
docker-compose build
```

### Next we setting environment.

Rename file .env.example to .env and add value of TELEGRAM_TOKEN. 

Example with popular "nano" text editor from project directory.

```sh
cd config
mv .env.example .env
nano .env
```

### Ready to run!

```sh
docker-compose up
```

After than, you can send message your bot and receive image to chat.

>Note: image save to file  inside of docker container. After of run that file at once be not exists. Worker save it throuth few minutes. 