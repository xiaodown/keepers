#!/bin/bash

# Creates test users with public/private keypairs

howmany=$1
LOGFILE="/root/usergen/log.$(date --iso-8601=minutes)"


log_setup() {

    exec > >(tee -a $LOGFILE)
    exec 2>&1

}

create_group() {

    if [ ! getent group testgroup ] ;then
        groupadd -f testgroup
    fi

}

prep_work() {

    if [ "$(whoami)" != "root" ] ;then
        echo "you must be root or this script won't work"
        exit 1
    fi

    cd /root/
    mkdir /root/usergen
    mkdir /tmp/privatekeys

    log_setup
    create_group

}

log() {

    echo "[$(date --rfc-3339=seconds)]: $*"

}

create_user() {

    user="testuser${1}"
    sshdir="/home/$user/.ssh"

    log "creating $user"
    useradd -G testgroup -m -N $user

    log "creating SSH keypair for $user in $sshdir"
    mkdir $sshdir
    chmod 700 $sshdir
    ssh-keygen -b 2048 -t rsa -f ${sshdir}/id_rsa -q -N ""
    cp $sshdir/id_rsa.pub $sshdir/authorized_keys
    chmod 600 $sshdir/authorized_keys
    chown -R $user $sshdir
    chgrp -R testgroup $sshdir
    cp $sshdir/id_rsa /tmp/privatekeys/$user

}

tarball_keys() {

    log "making tarball of private keys"
    cd /tmp/
    tar -cvf privatekeys.tar ./privatekeys
    gzip privatekeys.tar
    rm -rf /tmp/privatekeys
    mv privatekeys.tar.gz /root/usergen/privatekeys.$(date +%s).tar.gz

}

teardown() {

    echo "hi"

}

usage() {

    echo
    echo "  $0 - creates test unix users with ssh keys for testing purposes."
    echo
    echo "  Usage: $0 {<num>|teardown}"
    echo
    echo "       <num>    - the number of test users to create"
    echo "       teardown - will remove testuser* from the system"
    echo
    echo "       Note: either <num> or the string 'teardown' is required."
    echo
    exit 0

}

if [ "x$1" = "x" ] ;then
     usage
elif [ "$1" = "teardown" ] ;then
    teardown
    exit 0
fi

prep_work

for i in $(seq 1 ${howmany}) ;do
    create_user $i
done

tarball_keys

