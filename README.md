
<div align="center">

# whoswho

<br/><br/>
<img
alt="Header Image"
src="https://raw.githubusercontent.com/astrogewgaw/logos/main/rasters/whoswho.png"
/>
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
invoke statistics
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

[gitmoji]: https://gitmoji.dev
[license]: https://img.shields.io/github/license/astrogewgaw/whoswho?style=for-the-badge
[count]: https://img.shields.io/badge/Astrochemists-402-blueviolet?style=for-the-badge
[updated]: https://img.shields.io/badge/Last%20Updated-Monday%2031%20October,%202022%2002:27:49%20am%20UTC-purple?style=for-the-badge
[gitmoji-badge]: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=for-the-badge
[tweeters]: https://img.shields.io/badge/Tweeters-55-blue?style=for-the-badge&logo=twitter
[contactable]: https://img.shields.io/badge/Contactable-298-darkgreen?style=for-the-badge&logo=gmail

</div>
