#!/bin/bash

PROJECT_NAME="remeshing-project"

# 1. Change this to the directory containing the input files
SCRIPTS_ROOT=$HOME/$PROJECT_NAME/scripts

# 2. Fill in this list with the input scripts you want to run
SCRIPTS=(
    "$SCRIPTS_ROOT/ball-wall/3D.json"
    "$SCRIPTS_ROOT/masticator/3D.json"
    "$SCRIPTS_ROOT/twisting-beam/twisting-beam.json"
    # "$SCRIPTS_ROOT/spikes3d/drop-ball.json"
    "$SCRIPTS_ROOT/spikes3d/restart_031.json"
    "$SCRIPTS_ROOT/rollers/monkey-soft-hard.json"
)

# 3. Change this to the directory containing the output files
LOGS_DIR=$SCRATCH/${PROJECT_NAME}-results/logs
mkdir -p $LOGS_DIR

FILE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
JOB=$FILE_DIR/job.sh

TIME_STAMP=$(date +%Y_%m_%d_%H_%M_%S_%3N)

for (( i=0; i<${#SCRIPTS[*]}; ++i )); do
    JOB_NAME=$(basename "${SCRIPTS[$i]%.*}")
    SCRIPT_LOG_DIR="$LOGS_DIR/$(dirname $(realpath --relative-to="$SCRIPTS_ROOT" "${SCRIPTS[$i]}"))/${JOB_NAME}"
    mkdir -p "$SCRIPT_LOG_DIR"
    sbatch \
        --mem=32GB \
     	-J "${JOB_NAME}" \
        -o "${SCRIPT_LOG_DIR}/${TIME_STAMP}.out" -e "${SCRIPT_LOG_DIR}/${TIME_STAMP}.err" \
        "$JOB" "${SCRIPTS[$i]}"

    for NREF in 0 1 2 3; do
        NOREMESH_SCRIPT="${SCRIPTS[$i]%.*}-noremesh-nref${NREF}.${SCRIPTS[$i]##*.}"

        if [ -f "${NOREMESH_SCRIPT}" ]; then
        if (( $NREF == 3 )) ; then
            MEM="200GB"
        else
            MEM="40GB"
        fi
            JOB_NAME="nr${NREF}_$(basename "${SCRIPTS[$i]%.*}")"
            NOREMESH_SCRIPT_LOG_DIR="${SCRIPT_LOG_DIR}-noremesh-nref${NREF}"
            mkdir -p "$NOREMESH_SCRIPT_LOG_DIR"
            sbatch \
                --mem=${MEM} \
                -J "${JOB_NAME}" \
                -o "${NOREMESH_SCRIPT_LOG_DIR}/${TIME_STAMP}.out" -e "${NOREMESH_SCRIPT_LOG_DIR}/${TIME_STAMP}.err" \
                "$JOB" "$NOREMESH_SCRIPT"
        fi
    done
done
