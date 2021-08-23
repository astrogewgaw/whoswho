# type: ignore

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
your system, you probably rummaged through the folders and saw a lot of YAML
files. These files power the entire Who's Who website, thanks to the awesome
[**Lowdefy**][lowdefy] framework. I use this script to build those YAML files
from a bunch of [**Mako**][mako] templates, locally serve the Who's Who app
(to see if everything is working as intended), and update my local copy of the
database that ultimately makes it into the [**Github repository**][repository].
This script also calculates a few statistics about the database, such as the
total number of astrochemists, how many can be contacted (via their email or
Twitter), and how many of them are tweeting.

We use the [**invoke**][invoke] package to power the entire script. **invoke**
is a framework for running use-defined *tasks*. These tasks can be anything:
Python functions, shell commands, etc. In this simplest scenario (which is what
we user here), all the user needs to do is define the tasks in a `tasks.py` file,
and then invoke any task using the `invoke` CLI. The settings for the `invoke`
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

import attr
import toml
import arrow
import pandas as pd

from invoke import task
from typing import Union
from pathlib import Path
from textwrap import dedent
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from mako.lookup import TemplateLookup
from rich.console import Console, RenderGroup


console = Console()


@attr.s(auto_attribs=True)
class Metadata(object):

    name: str
    email: str
    author: str
    license: str
    version: str
    description: str
    license_file: Union[str, Path]
    long_description: Union[str, Path]


@attr.s(auto_attribs=True)
class Directories(object):

    pages: Union[str, Path]
    public: Union[str, Path]
    templates: Union[str, Path]


@attr.s(auto_attribs=True)
class URLs(object):

    main: str
    repo: str
    data: str
    issues: str
    discussions: str


@attr.s(auto_attribs=True)
class Settings(object):

    pgctx: str

    gutter: str

    pgalign: str
    mnalign: str
    ttalign: str
    txalign: str

    bgcolor: str
    fgcolor: str

    bdfont: str
    hdfont: str
    ttfont: str


@attr.s(auto_attribs=True)
class Configuration(object):

    """"""

    urls: URLs
    meta: Metadata
    dirs: Directories
    settings: Settings

    def __rich__(self):
        pass

    @classmethod
    def load(cls):
        data = toml.load("config.toml")
        return cls(
            urls=URLs(**data["urls"]),
            meta=Metadata(**data["meta"]),
            dirs=Directories(
                **{
                    name: (Path.cwd() / value).resolve()
                    for (
                        name,
                        value,
                    ) in data["dirs"].items()
                }
            ),
            settings=Settings(**data["settings"]),
        )

    @property
    def pages(self):
        files = config.dirs.templates.glob("*.mako")
        return [f.stem for f in files if f.stem != "page"]


@attr.s(repr=False, auto_attribs=True)
class Statistics(object):

    """"""

    data: pd.DataFrame
    onfile: Union[str, Path]

    def __rich__(self):

        grid = Table.grid(expand=False)
        grid.add_column(justify="left")
        grid.add_column(justify="right")

        grid.add_row(f"[b]Total count:[/]", f"[b]{self.count}[/]")
        grid.add_row(f"[b]Last updated:[/]", f"[b]{self.updated}[/]")
        grid.add_row(f"[b]Astrochemists tweeting:[/]", f"[b]{self.tweeters}[/]")
        grid.add_row(f"[b]Contactable astrochemists:[/]", f"[b]{self.contactable}[/]")

        covs = Table.grid(expand=True)
        covs.add_column(justify="left")
        covs.add_column(justify="right")
        for key, val in self.coverages.items():
            covs.add_row(f"{key} Coverage:", f"[b]{val}[/] %")

        grid.add_row("[b]Data Coverage:[/]", Panel(covs))
        grid.add_row("[b]Mean Coverage:[/]", f"[b]{self.mean_coverage}[/] %")

        notes = """
        *   An astrochemist is considered **contactable** if they have an email they can
            be reached at or if they are on Twitter.
        *   The *Twitter* column is not taken into account while calculating the mean
            coverage, because it is an *optional* field.
        """

        return Panel(
            RenderGroup(
                Panel(
                    grid,
                    title="Statistics",
                    title_align="left",
                    padding=2,
                    expand=False,
                ),
                "\n",
                Panel(
                    Markdown(dedent(notes)),
                    title="Notes",
                    title_align="left",
                    padding=2,
                    expand=False,
                ),
            ),
            expand=True,
        )

    @classmethod
    def load(cls):
        onfile = config.dirs.public / "whoswho.csv"
        data = pd.read_csv(onfile, index_col=0)
        return cls(data=data, onfile=onfile)

    @property
    def updated(self):
        fmt = "dddd DD MMMM, YYYY hh:mm:ss a ZZZ"
        return arrow.get(self.onfile.stat().st_mtime).format(fmt)

    @property
    def columns(self):
        return list(self.data.columns)

    @property
    def count(self):
        return len(self.data.index)

    @property
    def contactable(self):
        rows = self.data.iterrows()
        flag = lambda r: any([pd.notna(r.Email), pd.notna(r.Twitter)])
        return len([row for _, row in rows if flag(row)])

    @property
    def tweeters(self):
        return self.data.Twitter.count()

    @property
    def coverages(self):
        coverage = lambda col: round((col.count() / self.count) * 100, 2)
        return pd.Series({col: coverage(self.data[col]) for col in self.columns})

    @property
    def mean_coverage(self):
        excludes = ["Twitter"]
        covsum = sum(cov for col, cov in self.coverages.items() if col not in excludes)
        covmean = covsum / (100 * (self.coverages.count() - len(excludes)))
        covmean = round(covmean * 100, 2)
        return covmean


config = Configuration.load()
statistics = Statistics.load()


@task
def help(c):

    """"""

    with console.pager(styles=True):
        console.print(
            Panel(
                Markdown(__doc__.format(**attr.asdict(config.urls)), justify="full"),
                padding=2,
                expand=True,
                title=f"[b]{config.meta.name}[/]: [i]{config.meta.description}[/]",
                title_align="left",
            )
        )


@task
def version(c):

    """"""

    console.print(f"[u]Version[/]: [b]{config.meta.version}[/]")


@task
def update(c):

    """"""

    with console.status(status="Updating database..."):
        path = config.dirs.public / "whoswho.json"
        if path.exists():
            time = arrow.get(path.stat().st_mtime)
            if (arrow.now() - time).days < 7:
                df = pd.read_csv(path.with_suffix(".csv"))
        else:
            df = pd.read_csv(config.urls.data)
            df.to_csv(path.with_suffix(".csv"))
            df.to_json(path, indent=4, orient="records")


@task(update)
def compile(c):

    """"""

    with console.status(status="Compiling templates..."):
        lookup = TemplateLookup(directories=[config.dirs.templates])
        for page in config.pages:
            pname = "".join([page, ".yaml"])
            tname = "".join([page, ".mako"])
            with open(config.dirs.pages / pname, "w+") as f:
                f.write(
                    lookup.get_template(tname).render(
                        pgid=page,
                        pages=config.pages,
                        statistics=statistics,
                        columns=statistics.columns,
                        **attr.asdict(config.settings),
                    )
                )


@task(update)
def stats(c):

    """"""

    with console.pager(styles=True):
        console.print(statistics)


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


@task
def readme(c):

    """"""

    readme = dedent(
        """
            <div align="center">

            # {name}

            <br/><br/>
            <img src="" alt="Github Header">
            <br/><br/>

            ![License][license]
            [![Gitmoji][gitmoji-badge]][gitmoji]

            ![Last Updated][updated]

            ![Count][count]
            ![Contactable][contactable]
            ![Tweeters][tweeters]

            </div>

            <br/>

            <div align="justify">

            {doc}

            [gitmoji]: https://gitmoji.dev
            [license]: https://img.shields.io/github/license/astrogewgaw/whoswho?style=for-the-badge
            [count]: https://img.shields.io/badge/Astrochemists-{count}-blueviolet?style=for-the-badge
            [updated]: https://img.shields.io/badge/Last%20Updated-{updated}-purple?style=for-the-badge
            [gitmoji-badge]: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=for-the-badge
            [tweeters]: https://img.shields.io/badge/Tweeters-{tweeters}-blue?style=for-the-badge&logo=twitter
            [contactable]: https://img.shields.io/badge/Contactable-{contactable}-darkgreen?style=for-the-badge&logo=gmail

            </div>
        """
    )

    with open("README.md", "w+") as f:
        f.write(
            readme.format(
                name=config.meta.name,
                doc=__doc__.strip(),
                count=statistics.count,
                tweeters=statistics.tweeters,
                contactable=statistics.contactable,
                updated=statistics.updated.replace(" ", "%20"),
            )
        )
