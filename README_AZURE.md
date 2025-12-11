# Розгортання на Azure VM з Azure MySQL

## Швидкий старт

### 1. Підготовка Azure MySQL

1. Створіть Azure MySQL сервер в Azure Portal
2. Запишіть дані підключення:

   - Server name: `your-server.mysql.database.azure.com`
   - Admin username: `admin@your-server`
   - Password: ваш пароль

3. Додайте IP адресу вашої VM до Firewall rules

4. Створіть базу даних:

```sql
CREATE DATABASE hospitalss CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Розгортання на VM

```bash
# Підключіться до VM
ssh username@your-vm-ip

# Скопіюйте файли (з локальної машини)
scp -r . username@your-vm-ip:/home/username/hospital-api

# Або клонуйте з Git
git clone your-repo
cd database-flask-lab5-2

# Запустіть скрипт розгортання
chmod +x deploy_azure.sh
./deploy_azure.sh

# Налаштуйте .env файл
cp env.example .env
nano .env
# Вставте дані Azure MySQL

# Перезапустіть сервіс
sudo systemctl restart hospital-api
```

### 3. Налаштування мережі

В Azure Portal:

1. Перейдіть до вашої VM → Networking
2. Додайте Inbound rule:
   - Port: 5000
   - Protocol: TCP
   - Action: Allow

### 4. Перевірка

- API: `http://your-vm-ip:5000/api/v1/`
- **Swagger**: `http://your-vm-ip:5000/swagger/` ⭐

## Структура файлів

- `deploy_azure.sh` - основний скрипт розгортання
- `quick_deploy.sh` - швидке оновлення після змін
- `env.example` - приклад конфігурації
- `azure_deployment_guide.md` - детальна інструкція

## Корисні команди

```bash
# Статус сервісу
sudo systemctl status hospital-api

# Логи
sudo journalctl -u hospital-api -f

# Перезапуск
sudo systemctl restart hospital-api
```

## Swagger документація

Після розгортання Swagger UI доступний за адресою:

```
http://your-vm-ip:5000/swagger/
```

Тут ви можете:

- Переглянути всі доступні API endpoints
- Протестувати API безпосередньо в браузері
- Переглянути моделі даних та схеми

## Підтримка

Детальні інструкції: `azure_deployment_guide.md`
