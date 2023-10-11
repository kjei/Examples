# import ip
import os
import glob
import shutil
import logging
from glob import glob
import numpy as np

from popt.loop.optimize import Optimize
from simulator.opm import flow
from input_output import read_config
from popt.update_schemes.enopt import EnOpt
from popt.cost_functions.ecalc_npv import ecalc_npv

from enopt_plot import plot_obj_func

np.random.seed(101122)


def main():
    # Check if folder contains any En_ files, and remove them!
    for folder in glob('En_*'):
        try:
            if len(folder.split('_')) == 2:
                int(folder.split('_')[1])
                shutil.rmtree(folder)
        finally:
            pass
    for f in os.listdir('./'):
        if 'debug_analysis_step_' in f:
            os.remove(f)

    ko, kf = read_config.read_txt('init_optim.popt')
    ke = ko

    sim = flow(kf)
    method = EnOpt(ko, ke, sim, ecalc_npv, optimizer='GA')

    optimization = Optimize(method)
    optimization.run_loop()

    # Post-processing: enopt_plot
    plot_obj_func()

    # Display results
    state_initial = np.load('ini_state.npz', allow_pickle=True)
    state_final = np.load('opt_state.npz', allow_pickle=True)
    for f in state_initial.files:
        print('Initial ' + f + ' ' + str(state_initial[f]))
        print('Final ' + f + ' ' + str(state_final[f]))
        print('---------------')


if __name__ == '__main__':
    main()
