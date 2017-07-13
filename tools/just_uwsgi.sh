#!/bin/bash

#HackGirlfriend-测试服
echo "从 Windows-bash 部署-HackGirlfriend-测试服 @Tencent 118.89.27.96"
ssh -i /mnt/c/Developer/workspaces/密钥/for_danceiny ubuntu@118.89.27.96 '
    cd /home/ubuntu/web2/HackGirlfriend
    echo "-----------强制更新代码-----------"
    git fetch --all
    git reset --hard origin/dev
    echo "-----------重启uwsgi-----------"
    sudo killall -9 -u "www-data" uwsgi
    sudo /home/ubuntu/web2/bin/uwsgi --ini /home/ubuntu/web2/HackGirlfriend/PackageData/uwsgi.ini &
    echo "-----------重启uwsgi成功，结束-----------"
    exit
'