#!/bin/bash

# Скрипт розгортання Flask додатку на Azure VM
# Використання: ./deploy_azure.sh

set -e

echo "=== Розгортання Flask додатку на Azure VM ==="

# Оновлення системи
echo "Оновлення системи..."
sudo apt-get update
sudo apt-get upgrade -y

# Встановлення Python та залежностей
echo "Встановлення Python та залежностей..."
sudo apt-get install -y python3 python3-pip python3-venv mysql-client

# Встановлення системних залежностей для MySQL
sudo apt-get install -y default-libmysqlclient-dev build-essential pkg-config

# Створення директорії для додатку
APP_DIR="/opt/hospital-api"
echo "Створення директорії $APP_DIR..."
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Копіювання файлів (якщо ви вже на VM, використовуйте git або scp)
echo "Копіювання файлів..."
# Припускаємо, що файли вже скопійовані в поточну директорію
cp -r . $APP_DIR/
cd $APP_DIR

# Створення віртуального середовища
echo "Створення віртуального середовища..."
python3 -m venv venv
source venv/bin/activate

# Встановлення Python залежностей
echo "Встановлення Python залежностей..."
pip install --upgrade pip
pip install -r requirements.txt

# Створення .env файлу (якщо не існує)
if [ ! -f .env ]; then
    echo "Створення .env файлу з прикладу..."
    cp .env.example .env
    echo "ВАЖЛИВО: Відредагуйте .env файл з правильними даними Azure MySQL!"
    echo "Файл знаходиться в: $APP_DIR/.env"
fi

# Створення systemd service
echo "Створення systemd service..."
sudo tee /etc/systemd/system/hospital-api.service > /dev/null <<EOF
[Unit]
Description=Hospital Management API
After=network.target

[Service]
Type=notify
User=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 --access-logfile - --error-logfile - app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Перезавантаження systemd та запуск сервісу
echo "Запуск сервісу..."
sudo systemctl daemon-reload
sudo systemctl enable hospital-api
sudo systemctl start hospital-api

# Перевірка статусу
echo "Перевірка статусу сервісу..."
sleep 3
sudo systemctl status hospital-api --no-pager

echo ""
echo "=== Розгортання завершено! ==="
echo "API доступне за адресою: http://$(curl -s ifconfig.me):5000"
echo "Swagger документація: http://$(curl -s ifconfig.me):5000/swagger/"
echo ""
echo "Корисні команди:"
echo "  Перегляд логів: sudo journalctl -u hospital-api -f"
echo "  Перезапуск: sudo systemctl restart hospital-api"
echo "  Статус: sudo systemctl status hospital-api"
echo ""
echo "ВАЖЛИВО: Налаштуйте Azure NSG (Network Security Group) для відкриття порту 5000!"

