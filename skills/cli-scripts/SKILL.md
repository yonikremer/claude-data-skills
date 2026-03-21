---
name: cli-scripts
description: Turn Python scripts into proper command-line tools using click or argparse. Use when you need scripts with arguments, options, flags, subcommands, help text, and input validation. Click is recommended for new code; argparse for stdlib-only environments.
license: MIT
metadata:
    skill-author: K-Dense Inc.
---

# CLI Scripts

## Running on Windows

All the examples in this document work on Windows. The `python` and `pip` commands are used in the same way. There is no need to use `chmod` or other Unix-specific commands. You can run the scripts from the Command Prompt (`cmd.exe`) or PowerShell.

```batch
:: Example from Command Prompt
python your_script.py --help
python your_script.py data.csv -o results.csv
```

## click (recommended)

```bash
pip install click
```

### Basic script

```python
import click

@click.command()
@click.argument('input_file')
@click.option('--output', '-o', default='out.csv', help='Output file path')
@click.option('--limit',  '-n', default=None, type=int, help='Max rows to process')
@click.option('--verbose','-v', is_flag=True, help='Enable verbose output')
def process(input_file, output, limit, verbose):
    """Process INPUT_FILE and write results to OUTPUT."""
    if verbose:
        click.echo(f"Reading {input_file}...")
    # your logic here

if __name__ == '__main__':
    process()
```

```bash
python script.py data.csv --output result.csv --limit 1000 --verbose
python script.py --help
```

### Argument and option types

```python
@click.argument('path', type=click.Path(exists=True))           # must exist
@click.argument('output', type=click.Path(writable=True))
@click.argument('count', type=int)

@click.option('--date',    type=click.DateTime(formats=['%Y-%m-%d']))
@click.option('--level',   type=click.Choice(['debug','info','warn','error']))
@click.option('--config',  type=click.File('r'))                 # open file object
@click.option('--tags',    multiple=True)                        # --tags a --tags b → ('a','b')
@click.option('--ratio',   type=float, default=0.8,
              show_default=True)                                  # shows default in --help
@click.option('--output',  type=click.Path(), required=True)     # required option
```

### Subcommands

```python
@click.group()
@click.option('--config', default='config.env', envvar='APP_CONFIG')
@click.pass_context
def cli(ctx, config):
    """Data pipeline tools."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config

@cli.command()
@click.argument('source')
@click.pass_context
def ingest(ctx, source):
    """Ingest data from SOURCE."""
    cfg = ctx.obj['config']
    click.echo(f"Ingesting {source} with config {cfg}")

@cli.command()
@click.option('--dry-run', is_flag=True)
def export(dry_run):
    """Export processed data."""
    if dry_run:
        click.echo("Dry run — no files written")

if __name__ == '__main__':
    cli()
```

```bash
python pipeline.py ingest s3://bucket/data.csv
python pipeline.py export --dry-run
python pipeline.py --help
python pipeline.py ingest --help
```

### Progress bars and prompts

```python
# Progress bar
with click.progressbar(items, label='Processing') as bar:
    for item in bar:
        process(item)

# User confirmation
click.confirm('Delete all records?', abort=True)  # abort=True raises Abort on No

# Prompt for missing input
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True)

# Echo with color
click.echo(click.style('Error: file not found', fg='red'), err=True)
click.echo(click.style('Done!', fg='green', bold=True))
click.secho('Warning', fg='yellow')    # shorthand

# Print to stderr
click.echo("error message", err=True)
```

### Environment variable support

```python
# Automatically read from env vars
@click.option('--db-url', envvar='DATABASE_URL', required=True)
@click.option('--api-key', envvar='API_KEY', required=True)

# Set prefix for all options
@click.command()
@click.pass_context
def cli(ctx):
    pass

# Or globally:
cli = click.Group(auto_envvar_prefix='MYAPP')
# MYAPP_DB_URL → --db-url
```

### Error handling

```python
@click.command()
@click.argument('input_file', type=click.Path(exists=True))
def process(input_file):
    try:
        run(input_file)
    except FileNotFoundError as e:
        raise click.ClickException(str(e))       # prints "Error: ..." and exits 1
    except KeyboardInterrupt:
        click.echo("\nAborted.", err=True)
        raise SystemExit(1)
```

## argparse (stdlib, no dependencies)

```python
import argparse

def build_parser():
    parser = argparse.ArgumentParser(
        description='Process data files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,  # show defaults
    )
    parser.add_argument('input',          help='Input file path')
    parser.add_argument('-o', '--output', default='out.csv',     help='Output path')
    parser.add_argument('-n', '--limit',  type=int, default=None,help='Max rows')
    parser.add_argument('-v', '--verbose',action='store_true',   help='Verbose')
    parser.add_argument('--level',
        choices=['debug','info','warn','error'], default='info')
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    run(args.input, args.output, args.limit, args.verbose)

if __name__ == '__main__':
    main()
```

### Subparsers (argparse)

```python
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command', required=True)

ingest_p = subparsers.add_parser('ingest', help='Ingest data')
ingest_p.add_argument('source')

export_p = subparsers.add_parser('export', help='Export data')
export_p.add_argument('--dry-run', action='store_true')

args = parser.parse_args()
if args.command == 'ingest':
    ingest(args.source)
elif args.command == 'export':
    export(args.dry_run)
```

## Making a Script Installable

Add to `pyproject.toml`:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mytools"
version = "0.1.0"
dependencies = ["click", "pandas"]

[project.scripts]
process-data = "mytools.cli:cli"      # entry point
ingest       = "mytools.ingest:main"
```

```bash
pip install -e .        # installs in editable mode
process-data --help     # now available as a command
```
