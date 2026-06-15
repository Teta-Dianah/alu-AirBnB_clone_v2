#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Install Nginx if not already installed
if ! dpkg -l | grep -q nginx; then
    apt-get update -y
    apt-get install -y nginx
fi

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

# Add hbnb_static alias to Nginx config if not already present
if ! grep -q "hbnb_static" /etc/nginx/sites-available/default; then
    sed -i '/server_name _;/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' \
        /etc/nginx/sites-available/default
fi

# Restart Nginx
service nginx restart

exit 0
