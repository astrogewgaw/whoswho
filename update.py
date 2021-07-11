"""
Update the whoswho database.
"""

if __name__ == "__main__":

    import pandas as pd  # type: ignore
    from textwrap import dedent

    pd.read_csv(
        dedent(
            """
            https://
            docs.google.com/
            spreadsheets/
            d/
            e/
            2PACX-1vQkbCd9kEllq5SpaH13VxJEtw1k7eN3VdFTQetTP7udL10I0U-erve4IqotzOhDlp9ug-7ANoFqGpka/
            pub?
            gid=690927575&
            single=true&
            output=csv
            """
        )
        .replace("\n", "")
        .strip()
    ).fillna("").to_json(
        "public/data.json",
        indent=4,
        orient="records",
    )
