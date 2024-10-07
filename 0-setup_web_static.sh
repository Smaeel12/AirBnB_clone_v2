#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static
apt update -y && apt upgrade -y
apt install nginx -y
service nginx start
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
# Heredoc
cat << END > /data/web_static/releases/test/index.html
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
END

ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/

cat > /etc/nginx/sites-available/airbnb << END
server {
    listen 80;
    listen [::]:80;

    root /data/web_static/current/;
    server_name mydomainname.tech;
    index index.html;

    location /hbnb_static {
        alias /data/web_static/current/;
        autoindex off;
    }
}
END

ln -sf /etc/nginx/sites-available/airbnb /etc/nginx/sites-enabled/default
nginx -s reload