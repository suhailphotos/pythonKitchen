# src/pythonkitchen/backup_jobs.py

import os
import json
import tarfile
import re
from pathlib import Path
import click


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        click.echo(f"Config file not found at {config_path}")
        raise click.Abort()
    with open(config_path, 'r') as f:
        return json.load(f)

def get_job(config: dict, job_name: str) -> dict:
    for job in config.get('bk_jobs', []):
        if job.get('name') == job_name:
            return job
    return None

def backup_job(config_path: Path, job_name: str) -> None:
    config = load_config(config_path)
    job = get_job(config, job_name)
    if not job:
        click.echo(f"No job named '{job_name}' in config.")
        raise click.Abort()

    dest = Path(os.path.expandvars(job['destination'])).expanduser()
    dest.mkdir(parents=True, exist_ok=True)
    method = job.get('method')
    sources = [Path(os.path.expandvars(src)).expanduser() for src in job.get('source', [])]

    if method == 'tar.gz':
        pattern = re.compile(rf"{re.escape(job_name)}-(\d+)\.tar\.gz$")
        versions = [int(m.group(1)) for f in dest.iterdir() if (m := pattern.match(f.name))]
        next_ver = max(versions) + 1 if versions else 1
        archive_path = dest / f"{job_name}-{next_ver}.tar.gz"

        with tarfile.open(archive_path, "w:gz") as tar:
            for src in sources:
                if not src.exists():
                    click.echo(f"Source not found: {src}")
                    continue
                try:
                    arcname = src.relative_to(Path.home())
                except ValueError:
                    arcname = src.name
                tar.add(str(src), arcname=str(arcname))
        click.echo(f"Backup created: {archive_path}")
    else:
        click.echo(f"Unknown backup method: {method}")
        raise click.Abort()


def restore_job(config_path: Path, job_name: str, version: int = None) -> None:
    config = load_config(config_path)
    job = get_job(config, job_name)
    if not job:
        click.echo(f"No job named '{job_name}' in config.")
        raise click.Abort()

    dest = Path(os.path.expandvars(job['destination'])).expanduser()
    method = job.get('method')

    if method == 'tar.gz':
        pattern = re.compile(rf"{re.escape(job_name)}-(\d+)\.tar\.gz$")
        archives = [(int(m.group(1)), f) for f in dest.iterdir() if (m := pattern.match(f.name))]
        if not archives:
            click.echo(f"No backups found in {dest}")
            raise click.Abort()
        archives.sort(key=lambda x: x[0])
        if version is None:
            ver, archive_file = archives[-1]
        else:
            matches = [item for item in archives if item[0] == version]
            if not matches:
                click.echo(f"No archive version {version} found.")
                raise click.Abort()
            ver, archive_file = matches[0]

        with tarfile.open(archive_file, "r:gz") as tar:
            tar.extractall(path=Path.home())
        click.echo(f"Restored version {ver} for job '{job_name}'.")
    else:
        click.echo(f"Unknown restore method: {method}")
        raise click.Abort()

