#!/bin/sh

LOCUST="/usr/local/bin/locust"

LOCUSTFILE_PATH=${LOCUSTFILE_PATH:-/locustfile.py}

LOCUST_OPTS="-f $LOCUSTFILE_PATH $LOCUST_TEST --host=$TARGET_HOST $ADD_OPTIONS"

LOCUST_MODE=${LOCUST_MODE:-standalone}

if [ "$LOCUST_MODE" = "master" ]; then

    if [ -z ${EXPECT_SLAVES} ] ; then
        echo "No expected slaves. Set EXPECT_SLAVES number to set custom slave number waiting condition."
        LOCUST_OPTS="$LOCUST_OPTS --master"
    else
        LOCUST_OPTS="$LOCUST_OPTS --master --expect-slaves $EXPECT_SLAVES"
    fi
    # LOCUST_OPTS="$LOCUST_OPTS --master"

elif [ "$LOCUST_MODE" = "worker" ]; then
    LOCUST_OPTS="$LOCUST_OPTS --slave --master-host=$LOCUST_MASTER"
fi

echo "$LOCUST $LOCUST_OPTS"
$LOCUST $LOCUST_OPTS
