#!/bin/bash

PROJECT_NAME="remeshing-project"

# 1. Change this to the directory containing the input files
SCRIPTS_ROOT=$SCRATCH/$PROJECT_NAME/scripts

# 2. Fill in this list with the input scripts you want to run
SCRIPTS=(
    # "$SCRIPTS_ROOT/ball-obstacle/2D-highres.json"
    # "$SCRIPTS_ROOT/ball-obstacle/2D.json"
    # "$SCRIPTS_ROOT/ball-wall/2D-highres.json"
    # "$SCRIPTS_ROOT/ball-wall/2D.json"
    # "$SCRIPTS_ROOT/ball-wall/3D.json"
    # "$SCRIPTS_ROOT/indenter/2D.json"
    # "$SCRIPTS_ROOT/masticator/3D.json"
    # "$SCRIPTS_ROOT/masticator/h=0.1.json"
    # "$SCRIPTS_ROOT/masticator/h=0.05.json"
    "$SCRIPTS_ROOT/unit-tests/sliding.json"
    # "$SCRIPTS_ROOT/twisting-beam.json"
)
JOB_NAMES=(
    # "ball-obstacle-2D-highres"
    # "ball-obstacle-2D"
    # "ball-wall-2D-highres"
    # "ball-wall-2D"
    # "ball-wall-3D"
    # "indenter-2D"
    # "masticator-3D"
    # "masticator-h=0.1"
    # "masticator-h=0.05"
    "sliding"
    # "twisting-beam"
)

# 3. Change this to the directory containing the output files
LOGS_DIR=$SCRATCH/$PROJECT_NAME/logs
mkdir -p $LOGS_DIR

FILE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
JOB=$FILE_DIR/job.sh

TIME_STAMP=$(date +%Y_%m_%d_%H_%M_%S_%3N)

for (( i=0; i<${#SCRIPTS[*]}; ++i )); do
    JOB_NAME="${JOB_NAMES[$i]}"
    sbatch \
        -J "$JOB_NAME" \
        -o "$LOGS_DIR/$JOB_NAME-$TIME_STAMP.out" -e "$LOGS_DIR/${JOB_NAME}-${TIME_STAMP}.err" \
        "$JOB" "${SCRIPTS[$i]}"
done
