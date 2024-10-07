# HTML content for index.html
$indexfile = @(END)
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
END

# Nginx configuration content
$nginxconfig = @(END)
server {
  listen 80;
  listen [::]:80;

  root /data/web_static/current/;
  server_name _;
  index index.html;

  location /hbnb_static {
    alias /data/web_static/current/;
    autoindex off;
  }
}
END

# Update and upgrade system packages
exec { 'apt update':
  command => '/usr/bin/apt update -y',
}

exec { 'apt upgrade':
  command => '/usr/bin/apt upgrade -y',
  require => Exec['apt update'],
}

# Ensure Nginx is installed
package { 'nginx':
  ensure  => 'installed',
  require => Exec['apt upgrade'],
  before  => Service['nginx']
}

# Ensure Nginx service is running and enabled
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  require   => Package['nginx'],
  subscribe => File['/etc/nginx/sites-enabled/default']
}

# Create the necessary directory structure using the file resource
file { '/data':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

exec { '/usr/bin/mkdir -p /data/web_static/shared/':
  require => File['/data'],
}

exec { 'dir test':
  command => '/usr/bin/mkdir  -p /data/web_static/releases/test/',
  require => File['/data'],
}

# Create the index.html file with the specified content
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => $indexfile,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => Exec['dir test'],
}

# Create a symbolic link to the current release
file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test/',
  require => Exec['dir test']
}

# Place the Nginx config file in the correct location
file { '/etc/nginx/sites-available/airbnb':
  ensure  => 'present',
  content => $nginxconfig,
  require => Package['nginx'],
}

file { '/etc/nginx/sites-enabled/default':
  ensure  => 'link',
  target  => '/etc/nginx/sites-available/airbnb',
  require => File['/etc/nginx/sites-available/airbnb'],
}
