# 🎵 Music Supporter Bot for Telegram

Бот для поиска треков, текстов песен и новинок музыки через Spotify и Genius API. [Бот находится тут](https://t.me/mserbot)

## 🚀 Возможности
- Поиск **треков** по названию или отрывку текста песни
- Просмотр **текстов** песен
- Получение **информации** о треках (длительность, альбом, дата релиза)
- Подписка на **любимых исполнителей** и уведомление о **выходе** нового трека

## 🛠 Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/pomidorchik03/MSer
2. Установите пакеты:
   ```bash
   pip install -r requirements.txt
3. Заполните конфиг:
   ```bash
    #config.py
    TELEGRAM_TOKEN = "ваш_токен_бота"
    SPOTIFY_CLIENT_ID = "ваш_spotify_id"
    SPOTIFY_CLIENT_SECRET = "ваш_spotify_secret"
    GENIUS_ACCESS_TOKEN = "ваш_токен_genius"
    CHANNELL_TOKEN = "Токен_ТГ_канала_с_новыми_релизами"
    PROXIES = {
        "http": "http://USERNAME:PASSWORD@IP:PORT",
        "https": "http://USERNAME:PASSWORD@IP:PORT"
    }

## ⚙️Настройка API
1. Получите Ваш SPOTIFY_CLIENT_ID и SPOTIFY_CLIENT_SECRET:
   ```bash
   Зарегистрируйтесь на Spotify for Developers (https://developer.spotify.com)
   Создайте приложение и получите CLIENT_ID и CLIENT_SECRET
2. Получите Ваш GENIUS_ACCESS_TOKEN:
   ```bash
   Зарегистрируйтесь на docs.genius (https://docs.genius.com)
   Получите Ваш токен
3. Получите Ваш PROXIES:
   ```bash
   Зарегистрируйтесь на webshare.io (https://dashboard.webshare.io)
   Запишите в форму выше 
## 🔊Запуск
Для запуска приложения запустите **main.py**.
>***Учтите, что бот не работает в России без VPN!***

## 👨‍🎓Автор
[Shedoesacase](https://t.me/xxtsmx) (Илья)

[pomidorchik03](https://t.me/Shark766) (Буда)
