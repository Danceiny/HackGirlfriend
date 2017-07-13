supervisord，初始启动Supervisord，启动、管理配置中设置的进程。
sudo supervisorctl status  查看素有spawn进程的状态
supervisorctl stop programxxx，停止某一个进程(programxxx)，programxxx为[program:chatdemon]里配置的值，这个示例就是chatdemon。
supervisorctl start programxxx，启动某个进程
supervisorctl restart programxxx，重启某个进程
supervisorctl stop groupworker: ，重启所有属于名为groupworker这个分组的进程(start,restart同理)
supervisorctl stop all，停止全部进程，注：start、restart、stop都不会载入最新的配置文件。
supervisorctl reload，载入最新的配置文件，停止原有进程并按新的配置启动、管理所有进程。
supervisorctl update，根据最新的配置文件，启动新配置或有改动的进程，配置没有改动的进程不会受影响而重启
注意：显示用stop停止掉的进程，用reload或者update都不会自动重启。

http://yidao620c.github.io/2017/01/20/web/uwsgi.html

sudo supervisorctl status hello     -- 获取hello服务的状态，因为是autorstart，这里已经启动了
hello  RUNNING    pid 1159, uptime 0:20:32

sudo supervisorctl status hello     -- 获取hello服务的状态，因为是autorstart，这里已经启动了
hello  RUNNING    pid 1159, uptime 0:20:32
sudo supervisorctl stop hello       -- 停止hello服务
hello: stopped
sudo supervisorctl stop hello       -- 再次停止hello，会有错误信息
hello: ERROR (not running)
sudo supervisorctl start hello      -- 启动hello服务
hello: started

find / -name supervisor.sock
unlink /***/supervisor.sock

# 杀进程
选出所有pid：ps -ef|grep uwsgi|grep -v grep|awk '{print $2}'

ps -ef|grep uwsgi|grep -v grep|awk '{print $2}'|xargs kill -9

还需要过滤用户组：killall -9 -u "www-data" uwsgi
  
  
```bash
#!/bin/bash
case "$1" in
  start)
        psid=`ps aux|grep "uwsgi"|grep -v "grep"|wc -l`
        echo psid
        if [ $psid -gt 2 ];then
            echo "uwsgi is running!"
            exit 0
        else
            echo "Start uwsgi service [OK]"
            uwsgi --ini /etc/uwsgi/apps-enabled/www.website.com.ini
        fi
        ;;
  stop)
        killall -9 -u "www-data" uwsgi      # 过滤 用户组,防止误杀自己.
        echo "Stop uwsgi service [OK]"
        ;;
  restart)
        killall -9 -u "www-data" uwsgi      # 过滤 用户组,防止误杀自己.
        echo "Restart uwsgi service [OK]"
        uwsgi --ini /etc/uwsgi/apps-enabled/www.website.com.ini
        ;;
  *)
        echo "Usages: sh uwsgiserver.sh [start|stop|restart]"
        ;;
esac
```