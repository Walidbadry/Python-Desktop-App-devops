#!/bin/bash

# ==============================
# Nginx Auto Setup for App Updates
# ==============================

APP_NAME="my_app"
DEPLOY_DIR="/var/www/$APP_NAME"
NGINX_SITE="/etc/nginx/sites-available/$APP_NAME"
NGINX_ENABLED="/etc/nginx/sites-enabled/$APP_NAME"
SERVER_NAME="your-server.com"

echo "🚀 Setting up Nginx for $APP_NAME"

# 1. Create deploy directories
sudo mkdir -p "$DEPLOY_DIR/versions"
sudo chown -R $USER:$USER "$DEPLOY_DIR"

# 2. Create Nginx config file
sudo tee "$NGINX_SITE" > /dev/null <<EOF
server {
    listen 80;
    server_name $SERVER_NAME;

    root $DEPLOY_DIR;

    index index.html;

    location / {
        autoindex on;
        try_files \$uri \$uri/ =404;
    }

    # Allow direct download of installers
    location /versions/ {
        autoindex on;
    }

    # Serve latest.json with correct MIME
    location /latest.json {
        add_header Content-Type application/json;
    }

    error_log /var/log/nginx/${APP_NAME}_error.log;
    access_log /var/log/nginx/${APP_NAME}_access.log;
}
EOF

# 3. Enable site
sudo ln -sf "$NGINX_SITE" "$NGINX_ENABLED"

# 4. Test Nginx config
echo "🔍 Testing Nginx configuration..."
sudo nginx -t

# 5. Reload Nginx
echo "🔄 Reloading Nginx..."
sudo systemctl reload nginx

echo "✅ Nginx setup complete for $APP_NAME"
echo "📂 Deployment path: $DEPLOY_DIR"
echo "🌍 Access at: http://$SERVER_NAME/latest.json"
