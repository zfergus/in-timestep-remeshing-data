#!/bin/sh

POLYFEM_BIN=/home/zachary/Development/polyfem/build/release/PolyFEM_bin
INPUT=/home/zachary/Development/plasticity/scripts
OUTPUT=/home/zachary/Development/plasticity/output

SCENES=(
    # "unit-tests/1-square-dbc.json"
    # "unit-tests/1-square-rotating.json"
    # "golf-ball.json"
    "masticator/h=0.1.json"
)

for scene in "${SCENES[@]}"; do
    echo "Running scene: ${scene}"
    ${POLYFEM_BIN} -j "${INPUT}/${scene}" -o "${OUTPUT}/${scene%.*}"
done