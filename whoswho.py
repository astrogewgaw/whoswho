#!/usr/bin/env python

"""
"""

import sys
import click
import arrow  # type: ignore
import invoke  # type: ignore
import pandas as pd  # type: ignore

from pathlib import Path
from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown
from mako.template import Template  # type: ignore
from mako.lookup import TemplateLookup  # type: ignore


version = "1.0.0"
console = Console()
weblink = "https://whoswho.astrogewgaw.com"


def render_help():

    """"""

    return Panel(
        Markdown(__doc__, justify="full"),
        title=f"",
        title_align="left",
        expand=True,
        padding=2,
    )


def render_version():

    """"""

    return f"[u]Version[/]: [b]{version}[/]"


def write_template():

    """"""

    pass


def calculate_stats():

    """"""

    pass


@click.group(invoke_without_command=True)
@click.option("-h", "--help", is_flag=True, is_eager=True)
@click.option("-v", "--version", is_flag=True, is_eager=True)
def main(help: bool, version: bool):

    """"""

    if help:
        console.print(render_help())
        sys.exit(0)
    elif version:
        console.print(
            render_version(),
            highlight=False,
        )
        sys.exit(0)
    else:
        sys.exit(2)


@main.command()
def compile():

    """"""

    pass


@main.command()
def update():

    """"""

    pass


@main.command()
def stats():

    """"""

    pass


@main.command()
def serve():

    """"""

    pass


if __name__ == "__main__":
    main()