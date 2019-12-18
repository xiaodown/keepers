#!/bin/bash

# creates a thundering herd of SSH connectiosn
# assumptions: authorized_keys on target has key for source

target=$1
howmany=$2
log_dir="$(pwd)/$(basename $0)_logs/"
pid_dir="$(pwd)/$(basename $0)_pids/"

print_help() {

    echo
    echo "  $0 - creates a thundering herd of SSH connections"
    echo
    echo "  Usage: $0 <target> <number>"
    echo
    echo "      target - the hostanme of the ssh herd target box (required)"
    echo "      number - the number of ssh connections to attempt (required)"
    echo
    exit 0

}

mash() {

     for i in $(seq 1 ${howmany})
     do
        time ssh $target true &
     done 2>&1 | \
        stdbuf -i0 -o0 grep real | \
        stdbuf -i0 -o0 cut -c8- | \
        stdbuf -i0 -o0 sed 's/.$//'

}

prepare_to_mash() {

    echo
    mkdir -p $pid_dir
    mkdir -p $log_dir
    if ! [ "$howmany" -eq "$howmany" ] 2>/dev/null ;then
        echo "ERROR: 2nd argument \"$howmany\" is not an integer" ;echo
        print_help
    fi

}

tunnel_mash() {

    echo "Spawning $howmany tunnels:"
    for i in $(seq 1 ${howmany}) ;do
        #real one below
        AUTOSSH_LOGFILE=$log_dir/autosshlog.${i}.log AUTOSSH_DEBUG=1 AUTOSSH_PIDFILE=${pid_dir}/pid_${i} \
            autossh -M 0 -f -N -R 12${i}:127.0.0.1:11${i} ${target} -g -o ServerAliveInterval=10 \
            -o ServerAliveCountMax=1 -o ExitOnForwardFailure=yes
        echo -n "."
    done 2>&1
    echo
    echo "$howmany tunnels created."

}

wait_for_keypress() {

    echo
    read -n 1 -s -r -p "Press any key to remove tunnels and exit..."

}

cleanup () {

    cd $pid_dir
    echo
    echo "Cleaning up $howmany tunnels..."
    for i in $(cat *) ;do
        echo -n "."
        kill -TERM -- -${i} 2>/dev/null
        sleep 0.01
        kill -9 -- -${i} 2>/dev/null
    done
    echo
    rmdir $pid_dir 2>/dev/null
    echo "Cleaning up stragglers...."
    killall autossh 2>/dev/null
    sleep 5
    killall autossh 2>/dev/null
    echo "Done."

}

if [ "x$2" = "x" ] ;then
    print_help
fi

trap cleanup SIGINT SIGTERM

prepare_to_mash
tunnel_mash
wait_for_keypress
cleanup

