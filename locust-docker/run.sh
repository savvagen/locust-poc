#!/usr/bin/env bash

LOCUST="/usr/local/bin/locust"
LOCUST_OPTS="-f scenarios/random_scenarios.py $LOCUST_TEST --host=$TARGET_HOST $ADD_OPTIONS"
LOCUST_MODE=${LOCUST_MODE:-standalone}

if [[ "$LOCUST_MODE" = "master" ]]; then

    if  [-z "$EXPECT_SLAVES"]; then
        LOCUST_OPTS="$LOCUST_OPTS --master"
    else
        LOCUST_OPTS="$LOCUST_OPTS --master --expect-slaves $EXPECT_SLAVES"
    fi
#    LOCUST_OPTS="$LOCUST_OPTS --master"

elif [[ "$LOCUST_MODE" = "worker" ]]; then
    LOCUST_OPTS="$LOCUST_OPTS --slave --master-host=$LOCUST_MASTER"
fi

echo "$LOCUST $LOCUST_OPTS"
$LOCUST $LOCUST_OPTS
