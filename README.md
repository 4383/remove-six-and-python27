# Sixectomy

Utility to safely remove `six` usages from your projects

[Python 2.7 will retire in Janury 1st 2020](https://pythonclock.org/). The aim
of this project is to help you to remove six usage from your code and give you
a code compatible with python 3 only.

## Summary

Depending on the size of your project it can be painful to remove all the
`six` occurence in your code due to possible [tone of calls](https://review.opendev.org/#/q/project:openstack/heat+branch:master+topic:drop-six-and-py27-support)
to the six's compatibility functions.

Sixectomy afford to you the possibility to remove `six` properly
and in a safely manner for your project by removing six by using:
- [the python symboles](https://docs.python.org/3/library/symbol.html)
- [the python AST](https://docs.python.org/3/library/ast.html).
- [the python parser](https://docs.python.org/3/library/parser.html).
- [the python tokenizer](https://docs.python.org/3/library/tokenize.html).

These modules usages ensure sixectomy to give to you a compatible and
fully runnable code similar to your previous version with six.

By introspecting six itself sixectomy retrieve the right python3 modules
to use and know what need to be replaced in your code.

Sixectomy is an alternative to regex usage, like `sed` or shell commands,
who could be used to remove six but which could give you a wrong
and unexecutable python code after replacements.

As a safety measure, Sixectomy will check that the reformatted code
still produces a valid AST that is equivalent to the original.

Also, you can only either simulate a removing or simply list six usage in your
project.

## When and why using Sixectomy

- To fully drop the python 2 support by removing six usages too;
- To avoid to use handcrafted regex and pseudo automatized shell commands;
- To avoid issues and uncompatible code has your output;
- To avoid to you to maintain a compatibility matrix between six and python 3;
- To avoid to spend a lot of time on a boring task;
- And the last but not the least, *to ensure that your code still works after*.

## Install

Install or upgrade to the latest version:

```sh
python3 -m pip install -U sixectomy
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
