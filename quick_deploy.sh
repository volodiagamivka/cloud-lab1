#!/bin/bash

# Швидкий скрипт для розгортання (для використання після першого розгортання)

set -e

APP_DIR="/opt/hospital-api"

echo "=== Швидке оновлення додатку ==="

cd $APP_DIR

# Активація віртуального середовища
source venv/bin/activate

# Оновлення залежностей
echo "Оновлення залежностей..."
pip install --upgrade pip
pip install -r requirements.txt

# Перезапуск сервісу
echo "Перезапуск сервісу..."
sudo systemctl restart hospital-api

echo "Готово! Перевірте статус: sudo systemctl status hospital-api"

