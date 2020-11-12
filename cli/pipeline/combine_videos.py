__all__ = ['combine_videos']

import os
import tempfile

from cli.structures import Job


def combine_videos(job: Job):
    input = job['converted']
    output = os.path.join(os.path.dirname(input[0]), f'{job["name"]}.mp4')

    with tempfile.NamedTemporaryFile(mode='w') as fp:
        for f in input:
            fp.write(f"file '{os.path.abspath(f)}'\n")
        fp.flush()

        os.system(f'ffmpeg -f concat -safe 0 -i {fp.name} -c copy "{output}"')

    return output
