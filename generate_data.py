
import argparse
import datetime
from pathlib import Path

import numpy as np
import yaml

from predictive_hands.data_loading.DataContainer import DataContainer


def generateData(cfg):
    if cfg['regenerate_data'] or not Path(cfg['data_path']).is_file():
        DataContainer.generateGRABData(cfg)

if __name__ == "__main__":

    msg = ''' 
        You know, some stuff at some point.
            '''

    parser = argparse.ArgumentParser(description='Train prediction')
    parser.add_argument('--directories_file', required=True, type=str,
                        help='Path to directories for given machine')
    parser.add_argument('--config_file', required=False, type=str,
                        help='Path to config file')
    parser.add_argument('--experiment_name', required=False, type=str,
                        help='Name of experiment (optional if provided in config)')

    args = parser.parse_args()

    current_config= args.config_file
    experiment_name = args.experiment_name


    if current_config is None:
        current_config = 'configs/default_config.yml'

    directories_cfg = yaml.full_load(open(args.directories_file, 'r'))
    cfg = yaml.full_load(open(current_config,'r'))

    cfg.update(directories_cfg)

    if experiment_name is not None:
        cfg['experiment_name'] = experiment_name

    if cfg['joint_noise_error'] is not None:
        cfg['joint_noise'] = cfg['joint_noise_error']*(np.sqrt(np.pi/8))
        cfg['transl_noise'] = cfg['transl_noise_error'] * (np.sqrt(np.pi / 8))


    cfg['experiment_dir'] = str(Path(cfg['exp_dir_base']).joinpath('experiments', cfg['experiment_name']))

    cfg['datetime'] = str(datetime.datetime.now())
    generateData(cfg)

