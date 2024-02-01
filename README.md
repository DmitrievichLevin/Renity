# Burgos Protocol Buffer

[![PyPI](https://img.shields.io/pypi/v/Burgos.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/Burgos.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/Burgos)][python version]
[![License](https://img.shields.io/pypi/l/Burgos)][license]

[![Read the documentation at https://Burgos.readthedocs.io/](https://img.shields.io/readthedocs/Burgos/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/DmitrievichLevin/Burgos/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/DmitrievichLevin/Burgos/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/Burgos/
[status]: https://pypi.org/project/Burgos/
[python version]: https://pypi.org/project/Burgos
[read the docs]: https://Burgos.readthedocs.io/
[tests]: https://github.com/DmitrievichLevin/Burgos/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/DmitrievichLevin/Burgos
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

There are many ways to optimize data transimission over the wire, but one of
the biggest impacts can be made from simply not sending data you don't need.
Burgos provides an Interface for rapidly defining the serialization format for
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

You can install _Burgos_ via [pip] from [PyPI]:

```console
$ pip install burgos
```

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Burgos_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

[pypi]: https://pypi.org/
[file an issue]: https://github.com/DmitrievichLevin/Burgos/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/DmitrievichLevin/Burgos/blob/main/LICENSE
[contributor guide]: https://github.com/DmitrievichLevin/Burgos/blob/main/CONTRIBUTING.md
[command-line reference]: https://Burgos.readthedocs.io/en/latest/usage.html
