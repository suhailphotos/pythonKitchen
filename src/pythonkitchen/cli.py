# src/pythonkitchen/cli.py

import os
import sys
import click
from pathlib import Path
from pythonkitchen.backup_jobs import backup_job, restore_job


def get_dropbox_dir() -> Path:
    """
    Determine the Dropbox directory:
    - Use $DROPBOX if set
    - On macOS: ~/Library/CloudStorage/Dropbox
    - On Windows: C:/Users/<User>/Dropbox
    - Otherwise: ~/Dropbox
    """
    env = os.getenv('DROPBOX')
    if env:
        return Path(env).expanduser()

    if sys.platform == 'darwin':  # macOS
        return Path.home() / 'Library' / 'CloudStorage' / 'Dropbox'
    elif sys.platform.startswith('win'):  # Windows
        return Path.home() / 'Dropbox'
    else:
        return Path.home() / 'Dropbox'


# Path to your backup configuration JSON
CONFIG_PATH = get_dropbox_dir() / 'matrix' / 'backups' / 'backup_config.json'

@click.group()
def main():
    """
    PythonKitchen CLI: backup and restore tasks defined in config.
    """
    pass

@main.command()
@click.option('--job', 'job_name', required=True, help='Name of the job defined in config.')
def backup(job_name):
    """Create a new versioned backup for the given job."""
    backup_job(CONFIG_PATH, job_name)

@main.command()
@click.option('--job', 'job_name', required=True, help='Name of the job defined in config.')
@click.option('--version', type=int, default=None, help='Version number to restore (default: latest).')
def restore(job_name, version):
    """Restore files for a given job and version."""
    restore_job(CONFIG_PATH, job_name, version)

if __name__ == '__main__':
    main()

