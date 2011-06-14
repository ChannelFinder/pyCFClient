#!/bin/bash

CHF_UPDATE_DIR=$PWD
NAME="$1"

[ -d $CHF_UPDATE_DIR ] || exit 1
echo $NAME

exec inoticoming \
--logfile $CHF_UPDATE_DIR/log/my.log \
$CHF_UPDATE_DIR/ \
--stderr-to-log --stdout-to-log \
--suffix '.dbl' \
--chdir $CHF_UPDATE_DIR \
cf-update-ioc {} \;
