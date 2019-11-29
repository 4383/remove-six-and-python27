# Sixectomy

Utility to remove `six` usages from your projects

[Python 2.7 will retire in Janury 1st 2020](https://pythonclock.org/). The aim
of this project is to help you to remove six usage from your code and give you
a code compatible with python 3 only.

Depending on the size of your project it can be painful to remove all the
`six` occurence in your code due to possible [tone of calls](https://review.opendev.org/#/q/project:openstack/heat+branch:master+topic:drop-six-and-py27-support)
to the six's compatibility functions.

Sixectomy afford to you the possibility to remove to remove `six` properly
and in a safely manner for your project by removing six by using the
[python AST](https://docs.python.org/3.8/library/ast.html).

As a safety measure, Sixectomy will check that the reformatted code
still produces a valid AST that is equivalent to the original.

Also, you can only either simulate a removing or simply list six usage in your
project.

## Install

```sh
python3 -m pip install sixectomy
```

## Usages

If no path is specified then sixectomy will inspect the current directory:

```sh
$ sixectomy
```

If you give a path at the CLI then sixectomy will inspect the given path:

```sh
$ sixectomy ~/<path-of-your-project>/
```
## Contribute

If you want to contribute to niet [please first read the contribution guidelines](CONTRIBUTING.md)

## Licence

This project is under the MIT License.

[See the license file for more details](LICENSE)
