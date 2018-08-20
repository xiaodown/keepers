#!/bin/bash

# Generates a file to stdout that looks like what
# you would get if you did a knife status -F j
# Will Dunn / CC BY

now_ticks=$(python -c 'import time; print time.time()')

if [ "X$1" = "X" ] ;then
    echo 
    echo "usage: $0 N [N....]"
    echo 
    echo "  Generates (to stdout) a json file in the style of knife status -F j,"
    echo "  with node entries that are N minutes behind now(), one entry per argv."
    echo ; echo "example:"
    echo ; echo "   $0 1 2 5 60"
    echo "  (output would be json showing 4 chef nodes: 1, 2, 5, and 60 min since last chef-client run)"
    echo
    exit 0
fi

counter=1
maxnum=$#


echo "["
echo "  {"

for i in "$@" ;do
    seconds_ago=$(( $i * 60 ))
    ohai_time=`bc <<< "${now_ticks}-${seconds_ago}"`
    cat <<EOF
    "name": "server${counter}.node",
    "chef_environment": "chef-env",
    "ip": "10.0.0.$counter",
    "ohai_time": $ohai_time,
    "platform": "ubuntu",
    "platform_version": "14.04" 
EOF

    if [ "$counter" -lt "$maxnum" ];then
        echo "  },"
        echo "  {"
    fi
    counter=$((counter+1))
done

echo "  }"
echo "]"
