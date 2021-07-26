"""
Update the whoswho database.
"""

README = """
<div align="center">

# Who's Who?

[![Netlify Status][deploy-status]][deploys]

![License][license]
![Count][count]
![Last Updated][updated]
[![Gitmoji][gitmoji-badge]][gitmoji]

## A list 📝 of astrochemists 🧪 from across the globe 🌏 !

</div>

<div align="justify">

This project is an open-source, version-controlled contact list for astrochemists across the globe. It started as a hand-written list that I maintained for several years. That all changed last year, when I floated the idea of converting it into a version that would be maintained by the community and hosted on the web. The idea got a lot of appreciation, particularly from fellow astrochemists. A previous version of this list was hosted on my personal website. The development has now shifted to a sub-domain, with the web application being powered by the brilliant [**lowdefy**][lowdefy] framework. The source code, which is just a bunch of YAML files, can be found [*here*][repo]. This project relies heavily on the support of both the open-source and astrochemical communities. If you are a fellow astrochemist yourself, consider adding, editing or updating the list using the form [*here*][edits].

</div>

[me]: https://astrogewgaw.com
[gitmoji]: https://gitmoji.dev
[lowdefy]: https://lowdefy.com
[whoswho]: https://whoswho.astrogewgaw.com
[edits]: https://whoswho.astrogewgaw.com/edit
[repo]: https://github.com/astrogewgaw/whoswho
[deploys]: https://app.netlify.com/sites/whoswho/deploys
[license]: https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge
[count]: https://img.shields.io/badge/Astrochemists-{count}-blueviolet?style=for-the-badge
[gitmoji-badge]: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=for-the-badge
[deploy-status]: https://api.netlify.com/api/v1/badges/ebd6006f-31b2-4fb4-bde0-b358aee83986/deploy-status
[updated]: https://img.shields.io/badge/Last%20Updated-{updated}-purple?style=for-the-badge
"""

if __name__ == "__main__":

    import os
    import arrow  # type: ignore
    import pandas as pd  # type: ignore

    df = pd.read_csv(os.environ["WHOSWHO_SHEET_URL"]).fillna("")
    df.to_json("public/data.json", indent=4, orient="records")
    count = len(df.index)
    updated = arrow.utcnow().format("dddd DD MMMM, YYYY hh:mm:ss a ZZZ")

    with open("README.md", "w+") as f:
        f.write(
            README.format(
                count=count,
                updated=updated.replace(" ", "%20").strip(),
            ).strip()
        )
