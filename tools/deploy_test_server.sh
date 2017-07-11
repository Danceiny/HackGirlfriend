#!/bin/bash

#HackGirlfriend-测试服
echo "从 Windows-bash 部署-HackGirlfriend-测试服 @Tencent 118.89.27.96"
ssh -i /mnt/c/Developer/workspaces/密钥/for_danceiny ubuntu@118.89.27.96 '
    cd /home/ubuntu/web2/HackGirlfriend
    echo "-----------更新代码-----------"
    git pull
    echo "-----------重启uwsgi-----------"
    sudo killall  -9 uwsgi
    sudo service supervisor restart
    echo "-----------重启uwsgi成功，结束-----------"
    exit
'
# netstat -ap | grep 9001 | grep CLOSE_WAIT|grep -v grep|cut -c 80-84 |xargs kill
#sudo killall  -9 uwsgi
#sudo service supervisor restart
#sudo supervisorctl reload