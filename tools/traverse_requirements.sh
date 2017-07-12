#!/bin/bash

echo "build requirements.txt for pip."

out_file=requirements.txt
tmp_file=tmp.txt
site_dir=$1

function scan_dir(){
        for file in `ls $1`
        do
                if [ -d $1"/"$file ]
                then
                        echo "pip freeze in cur dir..."$1
                        pip freeze >> $site_dir"/"$tmp_file
                #       echo "进入该目录:"$file
                        scan_dir $1"/"$file
                fi
        done
}

scan_dir $site_dir

#sort $site_dir"/"$out_file |uniq > $site_dir"/"$out_file

awk ' !x[$0]++' $site_dir"/"$tmp_file > $site_dir"/"$out_file

rm $site_dir"/"$tmp_file