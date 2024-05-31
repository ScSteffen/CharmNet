#!/bin/bash
# Interpreter declaration

#SBATCH -A name_of_account
#SBATCH -p name_of_partition
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1     # Number of tasks (cores) per node
#SBATCH --cpus-per-task=128     # Number of CPU cores per task

#SBATCH -J sn_study
#SBATCH --mem=200g
#SBATCH --time 1440:00
#SBATCH -o ./slurm_logs/singularity_hohlraum%j.txt
#SBATCH -e ./slurm_logs/singularity_hohlraum_err_%j.txt
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=mai@mail.com