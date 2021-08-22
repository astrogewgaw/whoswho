"""
This script is used to manage the [**Who's Who in Astrochemistry**][whoswho]
database, a contact list of astrochemists from around the globe. If you are
seeing this help message, you have probably cloned the original repository,
or an original fork of it, on your local machine. You have installed all the
dependencies (probably because you saw a `requirements.txt` file) and you
figured out how to display this help message. Whether you were just ideally
curious, or you were thinking of contributing, you will find all the answers
you desire here.

First of all, what does this script do? Well, if you have this repository on
your system, you probably rummaged through the folders and saw a lof of YAML
files. These files power the entire Who's Who website, thanks to the awesome
[**Lowdefy**][lowdefy] framework. I use this script to build those YAML files
from a bunch of [**Mako**][mako] templates, locally serve the Who's Who app
(to see if everything is working as intended), and update my local copy of the
database that ultimately makes it into the [**Github repository**][repository].
This script also calculates a few statistics about the database, such as the 
total number of astrochemists, how many can be contacted (via their website or
email or Twitter), and how many of them are tweeting.

We use the [**invoke**][invoke] package to power the entire script. [**invoke**]
[invoke] is a framework for running use-defined *tasks*. These tasks can be almost
anything: Python functions, shell commands, etc. In this simplest scenario (which
is what we user here), all the user needs to do is define the tasks in a `tasks.py`
file, and then invoke any task using the `invoke` CLI. The settings for the `invoke`
CLI are customized through the `invoke.yaml` file.

To see how the site looks, just type:

```bash
invoke serve
```

This will start a local server and serve the Who's Who web application. As you
carry out your changes, you will be able to see them show up instantly! To make
a change, it is recommended that you change the templates (in the `templates`
directory) rather than the YAML pages themselves (which you will find in the
`pages` directory), because otherwise all your changes will vanish anytime you
recompile your changes with:

```bash
invoke compile
```

Run the above command everytime you wish to see your changes show up in the YAML
files andf in the web application. You can check out some stats about the database
by typing:

```bash
invoke stats
```

If you wish to update your copy of the database, just run:

```bash
invoke update
```

[whoswho]: {main}
[issues]: {issues}
[repository]: {repo}
[discussions]: {discussions}
[lowdefy]: https://lowdefy.com
[invoke]: http://www.pyinvoke.org
[mako]: https://www.makotemplates.org
"""

import toml
import arrow  # type: ignore
import pandas as pd  # type: ignore

from invoke import task  # type: ignore
from pathlib import Path
from textwrap import dedent
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from mako.lookup import TemplateLookup  # type: ignore
from rich.console import Console, RenderGroup


console = Console()
config = toml.load("config.toml")
meta = config["meta"]

dirs = {
    name: (Path.cwd() / value).resolve()
    for (
        name,
        value,
    ) in config["dirs"].items()
}

urls = config["urls"]
settings = config["settings"]
settings["pages"] = [
    _.stem for _ in dirs["templates"].glob("*.mako") if _.stem != "page"
]


def statistics():

    """"""

    df = pd.read_csv(dirs["public"] / "whoswho.csv", index_col=0)

    # Fields that are marked as optional and should not be considered
    # when calculating data coverage statistics. Currently, the only
    # such column is the `Twitter` column.
    optionals = ["Twitter"]

    return {
        "fields": list(df.columns),
        "count": len(df.index),
        "contactable": len(
            [
                row
                for _, row in df.iterrows()
                if any(
                    [
                        pd.notna(row.Email),
                        pd.notna(row.Website),
                        pd.notna(row.Twitter),
                    ]
                )
            ]
        ),
        "tweeters": df.Twitter.count(),
        "updated": arrow.utcnow().format("dddd DD MMMM, YYYY hh:mm:ss a ZZZ"),
        "coverages": {
            name: round((df[name].count() / len(df.index)) * 100, 2)
            for name in list(df.columns)
        },
        "mean_coverage": round(
            (
                sum(
                    [
                        coverage
                        for (name, coverage,) in {
                            name: round(
                                (df[name].count() / len(df.index)) * 100,
                                2,
                            )
                            for name in list(df.columns)
                        }.items()
                        if name not in optionals
                    ]
                )
                / (100 * (len(list(df.columns)) - len(optionals)))
            )
            * 100,
            2,
        ),
    }


@task
def help(c):

    """"""

    with console.pager(styles=True):
        console.print(
            Panel(
                Markdown(__doc__.format(**urls), justify="full"),
                padding=2,
                expand=True,
                title=f"[b]{meta['name']}[/]: [i]{meta['description']}[/]",
                title_align="left",
            )
        )


@task
def version(c):

    """"""

    console.print(f"[u]Version[/]: [b]{meta['version']}[/]")


@task
def update(c):

    """"""

    with console.status(status="Updating database..."):
        path = dirs["public"] / "whoswho.json"
        if path.exists():
            time = arrow.get(path.stat().st_mtime)
            if (arrow.now() - time).days < 7:
                df = pd.read_csv(path.with_suffix(".csv"))
        else:
            df = pd.read_csv(urls["data"])
            df.to_csv(path.with_suffix(".csv"))
            df.to_json(path, indent=4, orient="records")


@task(update)
def compile(c):

    """"""

    with console.status(status="Compiling templates..."):
        lookup = TemplateLookup(directories=[dirs["templates"]])
        templates = (Path(dirs["templates"])).glob("*.mako")
        for template in templates:
            if template.stem != "page":
                with open(
                    Path(dirs["pages"])
                    / "".join(
                        [
                            template.stem,
                            ".yaml",
                        ]
                    ),
                    "w+",
                ) as f:
                    f.write(
                        lookup.get_template(template.name).render(
                            pgid=template.stem,
                            **settings,
                            **statistics(),
                        )
                    )


@task(update)
def stats(c):

    """"""

    stats = statistics()
    stats.pop("fields")
    coverages = stats.pop("coverages")
    mean_coverage = stats.pop("mean_coverage")

    grid = Table.grid(expand=False)
    grid.add_column(justify="left")
    grid.add_column(justify="right")

    for key, value in stats.items():
        grid.add_row(f"[u]{key.title()}:[/]", f"[b]{value}[/]")

    table = Table(
        *coverages.keys(),
        title="Who's Who Data Coverage",
        title_justify="center",
        show_lines=True,
        expand=True,
    )
    table.add_row(*[f"{_}%" for _ in coverages.values()])

    panel = Panel(
        RenderGroup(
            Panel(
                grid,
                title="Who's Who Statistics",
                expand=False,
            ),
            "\n",
            table,
            f"\n[u]Mean Coverage[/] = [b]{mean_coverage}[/]%\n",
            Panel(
                (
                    dedent(
                        """
                        * The `Twitter` column is not taken into account
                        while calculating the mean coverage, because it
                        is an optional field.
                        """
                    )
                    .replace("\n", " ")
                    .strip()
                ),
                expand=True,
            ),
        ),
        expand=True,
    )

    with console.pager(styles=True):
        console.print(panel)


@task(compile)
def serve(c):

    """"""

    c.run("npx lowdefy@latest dev")


@task
def clean(c):

    """"""

    c.run("rm -rf pages/*")
    c.run("rm -rf .lowdefy")
    c.run("rm -rf .mypy_cache")
