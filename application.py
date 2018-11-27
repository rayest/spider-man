import argparse
import logging

from configs.profiles import active_config_by_profile
from core.foundation.utils import pid
from core.scheduler_runner import run

parser = argparse.ArgumentParser()
parser.add_argument('--active_profile')
parser.add_argument('--log_path')

command_args, unknown = parser.parse_known_args()

active_profile = command_args.active_profile or 'default'

logger = logging.getLogger(__name__)

active_config_by_profile(active_profile, command_args)

if __name__ == '__main__':
    logger.info('Active profile is ' + active_profile)
    pid.write()
    run()
