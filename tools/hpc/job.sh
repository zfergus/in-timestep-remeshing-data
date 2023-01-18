#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --time=96:00:00
#SBATCH --mem=64GB

PROJECT_NAME="remeshing-project"

# Load modules
module purge
module load cmake/3.22.2 python/intel/3.8.6 gcc/10.2.0 hdf5/intel/1.12.0

# 1. Change this to the directory containing the input files
SCRIPTS_ROOT=$SCRATCH/$PROJECT_NAME/scripts
SCRIPT=$(realpath $1)
SCRIPT_REL=$(realpath --relative-to=$SCRIPTS_ROOT $SCRIPT)

OUTPUT_ROOT=$SCRATCH/$PROJECT_NAME/results

# Drop the extension from script
TIME_STAMP=$(date +%Y_%m_%d_%H_%M_%S_%3N)
OUTPUT_DIR="$OUTPUT_ROOT/${SCRIPT_REL%.*}/${TIME_STAMP}"
mkdir -p $OUTPUT_DIR

# 2. Change this to the directory containing the executable
BIN_DIR=$SCRATCH/polyfem/build/release/
BIN="PolyFEM_bin"

# 3. Save the commit hashes and git diff for reproducibility
cd $SCRIPTS_ROOT
git rev-parse HEAD > $OUTPUT_DIR/project_commit.txt
git diff > $OUTPUT_DIR/project_diff.patch

cd $BIN_DIR
git rev-parse HEAD > $OUTPUT_DIR/polyfem_commit.txt
git diff > $OUTPUT_DIR/polyfem_diff.patch

# Build in case
# make -j16

# Run job
./$BIN -j $SCRIPT -o $OUTPUT_DIR --log_level debug