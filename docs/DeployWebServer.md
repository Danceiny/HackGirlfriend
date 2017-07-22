## 服务器部署示例
以 腾讯云 Ubuntu 16 64bit 为例。

### Pre-requisites
- mysql-server / libmysqld
- nginx
- uwsgi
### Nginx + uWSGI + supervisor
nginx配置 uwsgi_pass, 可以是sock文件，可以是ip:port。
`pip install uwsgi`
`pip install supervisor`
/etc/nginx/conf.d/*.conf

uwsgi的配置文件socket=对应nginx的uwsgi_pass。

需要安装uwsgi-plugin-python。

uwsgi配置 uwsgi.ini:
```ini
socket = 
pythonpath = 
home = # venv / virtualenv / ...
plugin = python,http
...
```
### Common commands
- ps -ef | grep nginx
- service nginx start/reload/stop
- sudo ln -s nginx_uwsgi.conf /etc/nginx/conf.d/
