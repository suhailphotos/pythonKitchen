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

@main.command("export-project")
@click.option(
    "--root", "root", required=True, type=click.Path(exists=True, file_okay=False),
    help="Root folder to export (recursively)."
)
@click.option(
    "--output", "output_path", required=False, type=click.Path(file_okay=True, dir_okay=False, writable=True),
    help="Optional output file path. If not given, print to stdout."
)
@click.option(
    "--include-env", is_flag=True, default=False,
    help="Include .env files in export."
)
def export_project_cli(root, output_path, include_env):
    """
    Exports the folder structure and all relevant project files for context.
    """
    from pythonkitchen.project_export import export_project
    export_project(root, output_path=output_path, include_env=include_env)

if __name__ == '__main__':
    main()

