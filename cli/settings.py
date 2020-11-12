import os

_config: dict


def set_config(d: dict):
    global _config
    _config = d


def load_config(path: str):
    import yaml, click
    if os.path.exists(path):
        with open(path, 'r') as f:
            config = yaml.full_load(f)
            set_config(config)
    else:
        click.echo(f'Failed loading config at: {path}')


def storage_path() -> str:
    return os.path.expanduser(_config['storage_path'])


def destreamer_path() -> str:
    return destreamer()['path']


def destreamer() -> dict:
    return _config['destreamer']


def destreamer_output() -> str:
    return destreamer()['output'] if os.path.isabs(destreamer()['output']) \
        else os.path.join(storage_path(), destreamer()['output'])


def destreamer_exec() -> str:
    return os.path.join(destreamer_path(), 'build/src/destreamer.js')


def ffmpeg() -> dict:
    return _config['ffmpeg']


def job_path():
    return jobs()['path'] if os.path.isabs(jobs()['path']) else os.path.join(storage_path(), jobs()['path'])


def jobs():
    return _config['jobs']


def youtube():
    return _config['youtube']


def verbosity():
    return _config['verbosity']
