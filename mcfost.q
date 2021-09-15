#!/bin/bash
#SBATCH --nodes=1 --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --job-name=MCFOST_Loop
#SBATCH --output=MCFOST.qout
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=END
#SBATCH --mail-user=harrison.v1@live.com
#SBATCH --time=0-168:00:00
#SBATCH --mem=16G
#SBATCH --partition=sstar

echo "HOSTNAME = $HOSTNAME"
echo "HOSTTYPE = $HOSTTYPE"
echo Time is `date`
echo Directory is `pwd`

ulimit -s unlimited
export OMP_SCHEDULE="dynamic"
export OMP_NUM_THREADS=16
export OMP_STACKSIZE=2048m

echo "Starting MCFOST Loop"
./mcfost_loop.sh
