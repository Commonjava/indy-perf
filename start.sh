#!/bin/bash


SCRIPT=$(cd ${0%/*} && echo $PWD/${0##*/})
# THIS=`realpath ${0}`
DIR=`dirname ${SCRIPT}`

INDY_WORKDIR=${INDY_WORKDIR:-$PWD}

JMETER=${JMETER:-$HOME/apps/jmeter/current/bin/jmeter}
TEST=${JMETER_TEST:-$DIR/tests/build-simulation-existing.jmx}
LOG=${JMETER_LOG:-"$DIR/$(basename $TEST).log"}
PROPS=${JMETER_PROPS:-$DIR/inputs/properties/local5.properties}

rm -rf $DIR/test-downloads
rm -f $LOG

echo "Starting Indy..."
nohup $INDY_WORKDIR/bin/debug-launcher.rb 2>&1 > $PWD/indy-console.log &
INDY_PID=$!
echo "Indy console is logging to: ${PWD}/indy-console.log"

echo "Indy running in PID: ${INDY_PID}"

echo "Waiting for Indy startup to complete..."
while ! lsof -i -P | grep 8080 | grep LISTEN 2>&1 > /dev/null; do   
  ps ax | grep $INDY_PID | grep -v grep 2>&1 > /dev/null
  if [ $? -ne 0 ]; then
  	echo "Indy did not start properly."
  	exit 2
  fi

  sleep 0.1 # wait for 1/10 of the second before check again
done

#echo "Downloading Maven Central files (output is in $PWD/download.log)..."
#$DIR/populate-central.py 2>&1 > $PWD/download.log

read -p "Start tests? (NOTE: If you haven't started a profiler, you might want to now.) " yn
case $yn in
	[Yy]*) echo "Tests starting..."
		   break;;
	[Nn]*) echo "Shutting down Indy on PID: ${INDY_PID}..."
           kill -9 $INDY_PID
           exit;;
	*) echo "Please enter y/n."
       break;;
esac

echo "$JMETER -n -t $TEST -S $PROPS -l $LOG"
$JMETER -n -t $TEST -S $PROPS -l $LOG

