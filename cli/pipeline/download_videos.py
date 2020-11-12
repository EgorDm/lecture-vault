__all__ = ['download_videos']

import os

import click

from cli import settings
from cli.structures import Job


def download_videos(job: Job):
    output_dir = os.path.join(settings.destreamer_output(), f'{job["name"]}')
    os.makedirs(output_dir, exist_ok=True)

    inputs = ' '.join(job['input'])
    args = settings.destreamer().get("args", '')
    args += f' -t {settings.destreamer()["format"]}'

    click.echo('Starting video download')
    os.system(f'node {settings.destreamer_exec()} {args} -i {inputs} -o {output_dir}')

    return sorted([os.path.abspath(p) for p in os.listdir(output_dir)])
