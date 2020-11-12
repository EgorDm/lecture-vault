__all__ = ['convert_videos']

import multiprocessing
import os

from cli import settings
from cli.structures import Job


def convert_videos(job: Job):
    suffix = '.min'
    args = settings.ffmpeg()['args']
    files = [(file, f'{os.path.splitext(file)[0]}{suffix}.mp4') for file in job['downloads']]

    global process_file

    def process_file(file, out):
        if suffix in file or os.path.exists(out):
            print(f'Skipping file {file}')
            return
        print(f'Processing file: {file}')
        print(f'Output file {out}')

        os.system(f'ffmpeg -i "{file}" {args} "{out}"')
        return out

    pool = multiprocessing.Pool(settings.ffmpeg()['j'])
    return list(pool.starmap(process_file, files))
