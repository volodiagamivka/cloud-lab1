set -e

echo "deployment start"


sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip python3-venv mysql-client
sudo apt-get install -y default-libmysqlclient-dev build-essential pkg-config
APP_DIR="/opt/hospital-api"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

cp -r . $APP_DIR/
cd $APP_DIR

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt



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

sudo systemctl daemon-reload
sudo systemctl enable hospital-api
sudo systemctl start hospital-api

sleep 3
sudo systemctl status hospital-api --no-pager

echo ""
echo "=== finished ==="
echo "API : http://$(curl -s ifconfig.me):5000"
echo "Swagger: http://$(curl -s ifconfig.me):5000/swagger/"
echo ""


