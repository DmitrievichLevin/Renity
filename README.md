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

**Renity** is an [Open Source] Python Object-Binary-Mapper(OBM) _Binary Protocol Buffer_ that provides a way to rapidly define the de/serialization format of packets.

## Installation 🔧

You can install _Renity_ via [pip] from [PyPI]:

```console
$ pip install renity
```

## ✨ Features

- Improved throughput & reduced latency by reducing the data size transferred over the network
- Serialization & Deserialization
- Efficiency Compared to other formats like JSON & XML
- Strict schema definition(s) for messages
- Backward Compatible Schema(s)
- Development effort is reduced with an easy-to-use interface that creates a _Serialization Format_ from an Object Model.

## Example 📏

```python
import requests
from rentity import Message, StringField, IntField

class CustomMessage(Message):
        hello=StringField(default="World")
        sentence=ListField(StringField(required=True),IntField())

# Create a message
>>> example = CustomMessage({"sentence": ["Number of Apples:", 2]})

# Deserialized Message
>>> example.message
{"type": "CustomMessage", "hello": "World", "sentence": ["Number of Apples:", 2]}

# Serialized Message
>>> example.bytes
b"\x97\x88\rCustomMessage\x03\x92\x88\x05World\x8a\x88\x16\x92\x88\x11Number of Apples:\x88\x02"

# Post Serialized Message
>>> requests.post(url='http://example.com/message',
...                data=example.bytes,
...                headers={'Content-Type': 'application/octet-stream'})
...

# GET Example
>>> res = requests.get('http://example.com/message')
>>> response = CustomMessage(res.content)
>>> response.message
{"type": "CustomMessage", "hello": "World", "sentence": ["Number of Apples:", 2]}
```

## 🔬 Tests

It is recommended to set up Python 3.8, 3.9, 3.10 using [pyenv].

```shell
    # Install Poetry
    $ pip install poetry

    # Install Nox
    $ pip install nox

    # Install nox-poetry
    $ pip install nox-poetry

    # Install dependencies
    $ poetry install

    # Run Nox tests sessions
    $ nox --session


```

## Contributing 🧠

We welcome contributions of all types: from fixing typos to bug fixes to new features. For further questions about any of the below, please refer to the [Contributor Guide].
**Reach out**!
We encourage all contributors to reach out for work reference's. We're here to help and are available for any inquiries regarding our contributors!

## 🎓 Interactive Practice

Keep practicing so that your coding skills don't get rusty.

- ![Udemy](https://img.shields.io/badge/Udemy-A435F0?style=for-the-badge&logo=Udemy&logoColor=white)
- ![FreeCodeCamp](https://img.shields.io/badge/Freecodecamp-%23123.svg?&style=for-the-badge&logo=freecodecamp&logoColor=green)
- ![LeetCode](https://img.shields.io/badge/LeetCode-000000?style=for-the-badge&logo=LeetCode&logoColor=#d16c06)

## Usage

Please see the [Command-line Reference] for details.

## License

Distributed under the terms of the [Apache license][license],
_Renity_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

![Google](https://img.shields.io/badge/google-4285F4?style=for-the-badge&logo=google&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Godot Engine](https://img.shields.io/badge/GODOT-%23FFFFFF.svg?style=for-the-badge&logo=godot-engine)![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)![Steam](https://img.shields.io/badge/steam-%23000000.svg?style=for-the-badge&logo=steam&logoColor=white)

[pypi]: https://pypi.org/
[file an issue]: https://github.com/DmitrievichLevin/Renity/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/DmitrievichLevin/Renity/blob/main/LICENSE
[contributor guide]: https://github.com/DmitrievichLevin/Renity/blob/main/CONTRIBUTING.md
[command-line reference]: https://Renity.readthedocs.io/en/latest/usage.html
[apache license]: https://opensource.org/license/apache-2-0/
[open source]: https://opensource.org/license/apache-2-0/
[pyenv]: https://github.com/pyenv/pyenv
