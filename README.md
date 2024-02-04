# local-ip-bookkeeper

[![Build Status](https://github.com/psychonaute/local-ip-bookkeeper/workflows/test/badge.svg?branch=master&event=push)](https://github.com/psychonaute/local-ip-bookkeeper/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/psychonaute/local-ip-bookkeeper/branch/master/graph/badge.svg)](https://codecov.io/gh/psychonaute/local-ip-bookkeeper)
[![Python Version](https://img.shields.io/pypi/pyversions/local-ip-bookkeeper.svg)](https://pypi.org/project/local-ip-bookkeeper/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Keeps track of the device local ip, updating the registery in a gist. It make use of the [gist-storage](https://github.com/psychonaute/gist-storage) package

## Features

- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)

## Installation

```bash
poetry add git+git@github.com:psychonaute/local-ip-bookkeeper.git
```

## Usage

`GITHUB_GIST_TOKEN` environement variable needs to be defined with your githun token CF: [gist-storage doc](https://github.com/psychonaute/gist-storage)

`your-gist-hash` and `your-file.json` from the gist you manually created, which can be secret (private). Also CF: [gist-storage doc](https://github.com/psychonaute/gist-storage)

```python
from local_ip_bookkeeper.tracker import IPTracker

ip_tracker = IPTracker(
    'MSI Salticidae',
    '5df4f367d185e866235dc6e012761c3f',
    'info.json',
)
ip_tracker.update_ip()
# => gist .json should have new entry
# {
#     "Other Device": "192.168.4.150"
#     "MSI Salticidae": "192.168.4.155"
# }
```

## License

[MIT](https://github.com/psychonaute/local-ip-bookkeeper/blob/master/LICENSE)

## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [de5779cdb74d1f42b95f55e9ce6b80ebc5fe7c01](https://github.com/wemake-services/wemake-python-package/tree/de5779cdb74d1f42b95f55e9ce6b80ebc5fe7c01). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/de5779cdb74d1f42b95f55e9ce6b80ebc5fe7c01...master) since then.
