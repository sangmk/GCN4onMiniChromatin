# file handeling
import shutil
# import helper modules
import sys
import os
from pathlib import Path
# import ionerdss
absolute_path_to_add = os.path.expanduser('~/mankun/GitHub/ionerdss/')
# print(absolute_path_to_add)
# Add the absolute path to sys.path
sys.path.append(absolute_path_to_add)
import ionerdss as ion

def runjobs(N_rep, current_dir, subdir='', coordinate=True, simFirstIndex=1):
    workdir = current_dir + subdir
    # prepare an input directory and move input files inside
    # directory_input = workdir + '/nerdss_input/'
    # path = Path(directory_input)
    # if path.exists():
    #     shutil.rmtree(directory_input)  # Remove existing input files
    # path.mkdir(parents=True, exist_ok=True)  # Recreate empty
    # shutil.copy(current_dir+'/P.mol', directory_input)
    # shutil.copy(current_dir+'/S.mol', directory_input)
    # shutil.copy(current_dir+'/N.mol', directory_input)
    # if coordinate: shutil.copy(current_dir+'/fixCoordinates.pdb', directory_input)
    # shutil.copy(current_dir+'/parms.inp', directory_input)
    # use ionerdss to modify parameters
    model = ion.Simulation(workdir)
    sim_indices = [i+simFirstIndex for i in range(N_rep)]
    print(f'sim_indeces from {sim_indices[0]} to {sim_indices[-1]}')
    model.run_new_simulations(
        sim_indices=sim_indices, coordinate=coordinate, verbose=False, parallel=True,
        nerdss_dir='/home/msang2/mankun/nerdss_development/'
    )

# parent folder
pfolder = '/model/'
workdir = str(Path.cwd()) + f'{pfolder}/ka120_KDN8E4/'
runjobs(48, workdir, simFirstIndex=1)

import time

# Calculate the number of seconds in 3 days
seconds_in_3_days = 3 * 24 * 60 * 60

print(f"Program will pause for {seconds_in_3_days} seconds (3 days).")
time.sleep(seconds_in_3_days)