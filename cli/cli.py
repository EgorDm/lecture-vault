import os
from datetime import datetime

import click
import yaml

from cli import settings, pipeline
from cli.structures import Job


@click.group()
@click.option('--config', default=os.path.join(os.path.dirname(__file__), '../.config.yml'))
def cli(config):
    settings.load_config(config)


@cli.command()
@click.option('-j', '--job', default=None)
@click.option('-c', '--course', required=True)
@click.option('-n', '--lecture-no', default=None)
@click.option('-t', '--title', default=None)
@click.option('-s', '--subject', required=True)
@click.option('-d', '--date', default=datetime.today().strftime('%Y-%m-%d'))
@click.option('-u', '--url', multiple=True)
@click.option('-f', '--file', multiple=True)
@click.option('--run/--no-run', default=False)
@click.pass_context
def schedule(ctx, job, course, lecture_no, title, subject, date, url, file, run):
    if not title and not lecture_no:
        click.echo('Please specify either a title or a lecture no')
        exit(1)

    job_name = job if job else f'{course}_{date}_{lecture_no}'
    job_name = job_name if os.path.isabs(job_name) else os.path.join(settings.job_path(), job_name)

    job = Job(
        job_name if job_name.endswith('.yml') else job_name + '.yml',
        {
            'name': os.path.basename(job_name),
            'metadata': {
                'course': course,
                'lecture_no': lecture_no,
                'title': title if title else f'Lecture {lecture_no}',
                'subject': subject,
                'date': date
            },
            'input': list(url),
            'downloads': list(file)
        }
    )

    if not job.exists() or click.confirm('Do you want to overwrite current job?', default=False):
        job.write()
    click.echo(f'Written job to {job.path}')

    if run:
        ctx.invoke(run_single, job=job.path)


@cli.command()
@click.argument('job', type=click.Path(exists=True))
def download(job):
    job = Job(job)
    if len(job.get('downloads', [])) > 0:
        click.echo('Files seem to be already downloaded')
        return

    click.echo('Downloading corresponding files')
    job['downloads'] = pipeline.download_videos(job)
    job.write()
    click.echo('Downloaded corresponding files')


@cli.command()
@click.argument('job', type=click.Path(exists=True))
def convert(job):
    job = Job(job)
    if len(job.get('converted', [])) > 0:
        click.echo('Files seem to be already converted')
        return

    click.echo('Starting conversion')
    job['converted'] = pipeline.convert_videos(job)
    job.write()
    click.echo('Converted corresponding videos')


@cli.command()
@click.argument('job', type=click.Path(exists=True))
def combine(job):
    job = Job(job)
    if len(job['converted']) > 1:
        job['video'] = pipeline.combine_videos(job)
        job.write()
    else:
        click.echo('No file merging is needed.')
        job['video'] = job['converted'][0]
    job.write()


@cli.command()
@click.argument('job', type=click.Path(exists=True))
def upload(job):
    job = Job(job)
    click.echo('Starting video upload')
    job['upload'] = pipeline.upload_videos(job)
    job.write()
    click.echo('Uploaded corresponding videos')


@cli.command()
@click.argument('job', type=click.Path(exists=True))
@click.pass_context
def run_single(ctx, job):
    ctx.invoke(download, job=job)
    ctx.invoke(convert, job=job)
    ctx.invoke(combine, job=job)
    ctx.invoke(upload, job=job)
