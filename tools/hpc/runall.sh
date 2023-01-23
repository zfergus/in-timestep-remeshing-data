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
    # "$SCRIPTS_ROOT/ball-wall/3D_restart_200.json"
    # "$SCRIPTS_ROOT/indenter/2D.json"
    # "$SCRIPTS_ROOT/masticator/3D.json"
    # "$SCRIPTS_ROOT/masticator/3D-restart_065-reversed.json"
    # "$SCRIPTS_ROOT/masticator/h=0.1.json"
    # "$SCRIPTS_ROOT/masticator/h=0.05.json"
    # "$SCRIPTS_ROOT/unit-tests/sliding.json"
    # "$SCRIPTS_ROOT/twisting-beam/twisting-beam.json"
    "$SCRIPTS_ROOT/twisting-beam/release_253.json"
    # "$SCRIPTS_ROOT/spikes2d/spikes2d.json"
    # "$SCRIPTS_ROOT/spikes3d/spikes3d.json"
    # "$SCRIPTS_ROOT/spikes3d/drop-ball.json"
    # "$SCRIPTS_ROOT/spikes3d/drop-dinosaur.json"
    # "$SCRIPTS_ROOT/spikes3d/drop-monkey.json"
    # "$SCRIPTS_ROOT/rollers/monkey-hard-hard.json"
    # "$SCRIPTS_ROOT/rollers/monkey-hard-soft.json"
    # "$SCRIPTS_ROOT/rollers/monkey-soft-hard.json"
    # "$SCRIPTS_ROOT/popper/popper5-1.json"
    # "$SCRIPTS_ROOT/popper/popper5-1_back.json"
)

# 3. Change this to the directory containing the output files
LOGS_DIR=$SCRATCH/$PROJECT_NAME/logs
mkdir -p $LOGS_DIR

FILE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
JOB=$FILE_DIR/job.sh

TIME_STAMP=$(date +%Y_%m_%d_%H_%M_%S_%3N)

for (( i=0; i<${#SCRIPTS[*]}; ++i )); do
    JOB_NAME=$(basename "${SCRIPTS[$i]%.*}")
    SCRIPT_LOG_DIR="$LOGS_DIR/$(dirname $(realpath --relative-to="$SCRIPTS_ROOT" "${SCRIPTS[$i]}"))/${JOB_NAME}"
    mkdir -p "$SCRIPT_LOG_DIR"
    sbatch \
        -J "${JOB_NAME}" \
        -o "${SCRIPT_LOG_DIR}/${TIME_STAMP}.out" -e "${SCRIPT_LOG_DIR}/${TIME_STAMP}.err" \
        "$JOB" "${SCRIPTS[$i]}"

    JOB_NAME="nr_${JOB_NAME}"
    SCRIPT_LOG_DIR="${SCRIPT_LOG_DIR}-noremesh"
    mkdir -p "$SCRIPT_LOG_DIR"
    sbatch \
        -J "${JOB_NAME}" \
        -o "${SCRIPT_LOG_DIR}/${TIME_STAMP}.out" -e "${SCRIPT_LOG_DIR}/${TIME_STAMP}.err" \
        "$JOB" "${SCRIPTS[$i]%.*}-noremesh.${SCRIPTS[$i]##*.}"
done
