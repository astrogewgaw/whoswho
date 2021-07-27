"""
Update the whoswho database.
"""

if __name__ == "__main__":

    import os
    import re
    import arrow  # type: ignore
    import pandas as pd  # type: ignore

    # Get data from Google Sheet as a DataFrame.
    # Fill the `N/A` values with empty strings
    # for ease-of-display on the web.
    df = pd.read_csv(os.environ["WHOSWHO_SHEET_URL"]).fillna("")

    # Serialize data to JSON.
    df.to_json(
        "public/data.json",
        indent=4,
        orient="records",
    )

    # Get some stats from the data.
    count = len(df.index)
    updated = arrow.utcnow().format("dddd DD MMMM, YYYY hh:mm:ss a ZZZ")

    # Read in the README.
    with open("README.md", "r") as f:
        text = f.read()

    # Add stats to README as badges.
    with open("README.md", "w+") as f:
        text = re.sub(
            r"Updated-([a-zA-Z0-9%:,]+)-",
            f"Updated-{updated.replace(' ', '%20').strip()}-",
            re.sub(
                r"Astrochemists-(d)",
                f"Astrochemists-{count}",
                text,
            ),
        )
        f.write(text)
