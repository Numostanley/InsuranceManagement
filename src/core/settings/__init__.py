from .base import base_env_config


def get_settings_environment():
    # detect environment to load settings configuration
    if base_env_config['ENVIRONMENT'] == 'prod':
        ENV_SETTINGS = 'core.settings.prod'
    else:
        ENV_SETTINGS = 'core.settings.dev'
    return ENV_SETTINGS
