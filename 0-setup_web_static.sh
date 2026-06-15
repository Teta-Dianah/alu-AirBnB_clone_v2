#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Install Nginx if not already installed
apt-get install -y nginx 2>/dev/null

# Create required directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a test HTML file
cat > /data/web_static/releases/test/index.html << 'HTMLEOF'
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
HTMLEOF

# Remove existing symlink and recreate it
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Configure Nginx to serve /hbnb_static using alias directive
cat > /etc/nginx/sites-available/default << 'NGINXEOF'
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
	index index.html index.htm index.nginx-debian.html;
	server_name _;
	location /hbnb_static {
		alias /data/web_static/current/;
		index index.html index.htm;
	}
	location / {
		try_files $uri $uri/ =404;
	}
}
NGINXEOF

# Restart Nginx
service nginx restart

exit 0
