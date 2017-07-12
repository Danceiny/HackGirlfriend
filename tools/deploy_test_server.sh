#!/bin/bash

#HackGirlfriend-测试服
echo "从 Windows-bash 部署-HackGirlfriend-测试服 @Tencent 118.89.27.96"
ssh -i /mnt/c/Developer/workspaces/密钥/for_danceiny ubuntu@118.89.27.96 '
    cd /home/ubuntu/web2/HackGirlfriend
    echo "-----------强制更新代码-----------"
    git fetch --all
    git reset --hard origin/dev
    echo "-----------重启uwsgi-----------"
    sudo killall -9 uwsgi
    sudo service supervisor restart
    echo "-----------重启uwsgi成功，结束-----------"
    exit
'
# netstat -ap | grep 9001 | grep CLOSE_WAIT|grep -v grep|cut -c 80-84 |xargs kill
#sudo killall  -9 uwsgi
#sudo service supervisor restart
#sudo supervisorctl reload

#没有加入缓存区
#git checkout . && git clean -xdf
# 有的修改以及加入暂存区的话,那么
#git reset --hard
#git clean -xdf