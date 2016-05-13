#!/bin/bash

JMETER=${JMETER:-$HOME/apps/jmeter/current/bin/jmeter}
TEST=${JMETER_TEST:-$PWD/tests/build-simulation-existing.jmx}
LOG=${JMETER_LOG:-"$(basename $TEST).log"}
PROPS=${JMETER_PROPS:-$PWD/inputs/properties/local5.properties}

rm -rf $PWD/test-downloads
rm $LOG

echo "$JMETER -n -t $TEST -S $PROPS -l $LOG"
$JMETER -n -t $TEST -S $PROPS -l $LOG

