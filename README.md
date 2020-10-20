# A simple wrapper for `googletrans`

## Features
- default translate to Chinese
- file or text
- auto split with `nltk` when characters exceed 5000

## Installation
```bash
pip install simple-googletrans
```

## Usage
```python
from simple_googletrans import GoogleTrans

t = GoogleTrans()
t.translate('hello world')

t = GoogleTrans(url='translate.google.com', proxies={'https': 'https://127.0.0.1:1080'}, timeout=15)
t.translate('hello world', dest='fr')
```

### Command Line
```bash

gtranslate "hello world!"

gtranslate README.md

gtranslate README.md -o README.cn.txt

# list all languages
gtranslate -l

# use a proxy
gtranslate --proxy 181.211.145.46:8080 README.md

# other options
gtranslate -d fr hello world
```
