#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Install Nginx if not already installed
apt-get update -y
apt-get install -y nginx

# Create required directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file to test Nginx configuration
cat > /data/web_static/releases/test/index.html << 'HTML'
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
HTML

# Delete existing symlink and recreate it every time
rm -rf /data/web_static/current
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to the ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Write Nginx config with hbnb_static alias (overwrite for reliability)
cat > /etc/nginx/sites-available/default << 'NGINX'
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
NGINX

# Restart Nginx to apply the changes
service nginx restart

exit 0
