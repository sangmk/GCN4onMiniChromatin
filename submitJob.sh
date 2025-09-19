#!/bin/bash
#SBATCH --job-name=EquiSpatial
#SBATCH --time=72:0:0
#SBATCH --partition=parallel
#SBATCH --nodes=1
# number of tasks (processes) per node
#SBATCH --ntasks-per-node=48
#### load and unload modules you may need

module load gsl 

python runjobs.py

wait
# done
