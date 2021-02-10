# b3-data

<center>

[![PyPI - Version](https://badge.fury.io/py/b3-data.svg)](https://badge.fury.io/py/b3-data)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/b3-data)](https://pypi.org/project/b3-data/)
[![PyPI - License](https://img.shields.io/pypi/l/b3-data)](https://opensource.org/licenses/MIT)

</center>

b3-data is a Python package for dealing with https://b3.com.br data


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install b3-data.

```bash
pip install b3-data
```

## Usage

Download the latest file from their api:

```
$ b3-data download
downloading https://arquivos.b3.com.br/apinegocios/tickercsv/2020-12-05 to 2020-12-05.zip
```


Download specific date:

```
$ b3-data download --date 2020-12-04
downloading https://arquivos.b3.com.br/apinegocios/tickercsv/2020-12-04 to 2020-12-04.zip
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
