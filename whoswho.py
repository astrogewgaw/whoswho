"""
Copyright (c) 2021 Ujjwal Panda
"""

import json
import arrow  # type: ignore
import pandas as pd  # type: ignore

from pathlib import Path
from textwrap import dedent
from mako.lookup import TemplateLookup  # type: ignore


here = Path(__file__).parent.resolve()


def serve(name: str, **kwargs) -> str:

    """"""

    lookup = TemplateLookup(directories=[str(here / "templates")])
    template = lookup.get_template(name)
    pages = [_.name.replace(".yaml", "") for _ in (here / "pages").glob("*.yaml")]
    return template.render(pages=pages, **kwargs)


def download() -> pd.DataFrame:

    """"""

    df = pd.read_csv(
        dedent(
            """
            https://
            docs.google.com/
            spreadsheets/
            d/
            e/
            2PACX-
            1vQkbCd9kEllq5SpaH13VxJEtw1k7eN3VdFTQetTP7udL10I0U-
            erve4IqotzOhDlp9ug-
            7ANoFqGpka/
            pub?
            gid=690927575
            &single=true
            &output=csv
            """
        )
        .replace("\n", "")
        .strip()
    )

    return df


def stats(df: pd.DataFrame):

    """"""

    optionals = ["Twitter"]

    count = len(df.index)
    updated = arrow.utcnow().format("dddd DD MMMM, YYYY hh:mm:ss a ZZZ")
    coverages = {
        name: round(
            (df[name].count() / count) * 100,
            2,
        )
        for name in df.columns
    }
    mean_coverage = round(
        (
            sum(
                [
                    coverage
                    for (
                        name,
                        coverage,
                    ) in coverages.items()
                    if name not in optionals
                ]
            )
            / (100 * (len(df.columns) - len(optionals)))
        )
        * 100,
        2,
    )

    tweeters = df.Twitter.count()
    contactable = len(
        [
            row
            for _, row in df.iterrows()
            if pd.notna(row.Email) or pd.notna(row.Website) or pd.notna(row.Twitter)
        ]
    )

    return [
        count,
        updated,
        coverages,
        mean_coverage,
        tweeters,
        contactable,
    ]


def ready():

    """"""

    df = download()

    [
        count,
        updated,
        coverages,
        mean_coverage,
        tweeters,
        contactable,
    ] = stats(df)

    fields = list(df.columns)

    about = serve(
        "about.mako",
        count=count,
        updated=updated,
        tweeters=tweeters,
        coverages=coverages,
        contactable=contactable,
        mean_coverage=mean_coverage,
    )

    data = serve("data.mako", fields=fields)
    edits = serve("edits.mako", fields=fields)
    world_map = serve("world_map.mako")

    for page, name in [
        (about, "about"),
        (data, "data"),
        (edits, "edits"),
        (world_map, "world_map"),
    ]:
        with open(here / "pages" / "".join([name, ".yaml"]), "w+") as f:
            f.write(page.strip())

    df.to_csv("public/whoswho.csv")
    df.to_json("public/whoswho.json", indent=4, orient="records")