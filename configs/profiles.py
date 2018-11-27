from configs.config import BasicConfig
from .local_config import LocalConfig

profiles = {

    'default': LocalConfig
}


config = BasicConfig()


def active_config_by_profile(active_profile, command_args):
    config = profiles[active_profile]
    config.init_config(command_args)
