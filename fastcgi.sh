#!/bin/bash

PROJDIR="/home/yuming.zh/python/tairAppManager_work"
PIDFILE="$PROJDIR/site.pid"
SOCKET="$PROJDIR/site.sock"
LOGFILE="$PROJDIR/site.log"
ERRFILE="$PROJDIR/site.err"
#SOCKET="/tmp/mysite.sock"
PYTHON="/usr/bin/python"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi
${PYTHON} manage.py runfcgi method=prefork socket=${SOCKET} pidfile=${PIDFILE} minspare=1 maxspare=5 maxchildren=10 outlog=${LOGFILE} errlog=${ERRFILE}
chmod a+w site.sock
