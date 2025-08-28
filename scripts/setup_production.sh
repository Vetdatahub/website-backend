#!/bin/bash

# Production environment setup script
# Run this script on your DigitalOcean droplet to set up the environment

echo "🚀 Setting up VetDataHub production environment..."
echo "=================================================="

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system packages
echo "📦 Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib git

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /var/www/vetdatahub-backend
sudo chown $USER:$USER /var/www/vetdatahub-backend

# Create log directory
echo "📁 Creating log directory..."
sudo mkdir -p /var/log/django
sudo chown www-data:www-data /var/log/django

# Set up PostgreSQL
echo "🗄️ Setting up PostgreSQL..."
sudo -u postgres psql << EOF
CREATE DATABASE vetdatahub_prod;
CREATE USER vetdatahub_user WITH ENCRYPTED PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE vetdatahub_prod TO vetdatahub_user;
ALTER USER vetdatahub_user CREATEDB;
\q
EOF

# Clone repository (if not already cloned)
if [ ! -d "/var/www/vetdatahub-backend/.git" ]; then
    echo "📥 Cloning repository..."
    cd /var/www/vetdatahub-backend
    git clone https://github.com/Vetdatahub/vetdatahub-backend.git .
fi

# Set up Python virtual environment
echo "🐍 Setting up Python virtual environment..."
cd /var/www/vetdatahub-backend
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements-prod.txt

# Copy environment template
echo "⚙️ Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "❗ Please edit .env file with your production values:"
    echo "   nano .env"
    echo ""
    echo "Required variables to update:"
    echo "  - DJANGO_SECRET_KEY"
    echo "  - DB_PASSWORD"
    echo "  - DJANGO_ALLOWED_HOSTS"
fi

# Set up Gunicorn service
echo "🦄 Setting up Gunicorn service..."
sudo tee /etc/systemd/system/gunicorn.service > /dev/null << 'EOF'
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/vetdatahub-backend
Environment="PATH=/var/www/vetdatahub-backend/venv/bin"
EnvironmentFile=/var/www/vetdatahub-backend/.env
ExecStart=/var/www/vetdatahub-backend/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          vetdatahub.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Set up Gunicorn socket
sudo tee /etc/systemd/system/gunicorn.socket > /dev/null << 'EOF'
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF

# Set up Nginx configuration
echo "🌐 Setting up Nginx..."
sudo tee /etc/nginx/sites-available/vetdatahub-backend > /dev/null << 'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location /static/ {
        root /var/www/vetdatahub-backend;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        root /var/www/vetdatahub-backend;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/vetdatahub-backend /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Start and enable services
echo "🔄 Starting services..."
sudo systemctl daemon-reload
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl restart nginx
sudo systemctl enable nginx

# Set permissions
echo "🔐 Setting permissions..."
sudo chown -R www-data:www-data /var/www/vetdatahub-backend
sudo chmod -R 755 /var/www/vetdatahub-backend

echo ""
echo "✅ Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit /var/www/vetdatahub-backend/.env with your production values"
echo "2. Update server_name in /etc/nginx/sites-available/vetdatahub-backend"
echo "3. Run initial Django setup:"
echo "   cd /var/www/vetdatahub-backend"
echo "   source venv/bin/activate"
echo "   python manage.py migrate --settings=vetdatahub.settings.settings_prod"
echo "   python manage.py collectstatic --noinput --settings=vetdatahub.settings.settings_prod"
echo "   python manage.py createsuperuser --settings=vetdatahub.settings.settings_prod"
echo "4. Start Gunicorn: sudo systemctl start gunicorn"
echo "5. Check status: sudo systemctl status gunicorn nginx"
