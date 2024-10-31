# google_colab_tor_proxy

A Python package to install and configure Tor and Privoxy for anonymized browsing.

## Installation

```bash
pip install google_colab_tor_proxy

## Usage

To use the package in your Python script, you can do the following:

```python
import google_colab_tor_proxy import tor_proxy_setup

tor_proxy_setup()
```

This will install and configure Tor and Privoxy for you.

## Example

Here is an example of how to use the package in a script:

```python
import requests
from google_colab_tor_proxy import tor_proxy_setup

tor_proxy_setup()

proxies = {
    'http': 'http://localhost:8118',
    'https': 'http://localhost:8118',
}

response = requests.get('http://httpbin.org/ip', proxies=proxies)
print(response.json())
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
