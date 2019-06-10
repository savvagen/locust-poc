#!/usr/bin/env bash

LOCUST="/usr/local/bin/locust"
LOCUS_OPTS="-f scenarios/random_scenarios.py $LOCUST_TEST --host=$TARGET_HOST $ADD_OPTIONS"
LOCUST_MODE=${LOCUST_MODE:-standalone}

if [[ "$LOCUST_MODE" = "master" ]]; then

    if  [-z "$EXPECT_SLAVES"]; then
        LOCUS_OPTS="$LOCUS_OPTS --master"
    else
        LOCUS_OPTS="$LOCUS_OPTS --master --expect-slaves $EXPECT_SLAVES"
    fi
#    LOCUS_OPTS="$LOCUS_OPTS --master"

elif [[ "$LOCUST_MODE" = "worker" ]]; then
    LOCUS_OPTS="$LOCUS_OPTS --slave --master-host=$LOCUST_MASTER"
fi

echo "$LOCUST $LOCUS_OPTS"
$LOCUST $LOCUS_OPTS
