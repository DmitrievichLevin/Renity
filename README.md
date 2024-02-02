# Renity Protocol Buffer

[![PyPI](https://img.shields.io/pypi/v/Renity.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/Renity.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/Renity)][python version]
[![License](https://img.shields.io/pypi/l/Renity)][license]

[![Read the documentation at https://Renity.readthedocs.io/](https://img.shields.io/readthedocs/Renity/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/DmitrievichLevin/Renity/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/DmitrievichLevin/Renity/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/Renity/
[status]: https://pypi.org/project/Renity/
[python version]: https://pypi.org/project/Renity
[read the docs]: https://Renity.readthedocs.io/
[tests]: https://github.com/DmitrievichLevin/Renity/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/DmitrievichLevin/Renity
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

There are many ways to optimize data transimission over the wire, but one of
the biggest impacts can be made from simply not sending data you don't need.
Renity provides an Interface for rapidly defining the serialization format for
Network Traffic solely in Python. Using Schema's that closely resemble an
Object Relational Mapping(ORM) we are able to generate simple class definitions
that contain fields and methods to serlialze/parse to and from raw bytes.

## Advantages

- Extendable
- Backward Compatible Schema(s)
- Fast Parsing
- strict enforcement at the application level(optional)
- Optimize size of transmissions

## Example

```
    class CustomMessage(Message):
        hello=StringField(default="World")
        sentence=ListField(StringField(required=True),IntField())

    example = CustomMessage({"sentence": ["Number of Apples:", 2]})

    print(example.message)

    Output:
        {"hello": "World", "sentence": ["Number of Apples:", 2]}
```

## Features

- TODO

## Requirements

- TODO

## Installation

You can install _Renity_ via [pip] from [PyPI]:

```console
$ pip install renity
```

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [Apache license][license],
_Renity_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

[pypi]: https://pypi.org/
[file an issue]: https://github.com/DmitrievichLevin/Renity/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/DmitrievichLevin/Renity/blob/main/LICENSE
[contributor guide]: https://github.com/DmitrievichLevin/Renity/blob/main/CONTRIBUTING.md
[command-line reference]: https://Renity.readthedocs.io/en/latest/usage.html
[apache license]: https://opensource.org/license/apache-2-0/
