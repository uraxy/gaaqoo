# gaaqoo

[![Build Status](https://travis-ci.org/uraxy/gaaqoo.svg?branch=master)](https://travis-ci.org/uraxy/gaaqoo)
[![Code Health](https://landscape.io/github/uraxy/gaaqoo/master/landscape.svg?style=flat)](https://landscape.io/github/uraxy/gaaqoo/master)
[![Coverage Status](https://coveralls.io/repos/github/uraxy/gaaqoo/badge.svg?branch=master)](https://coveralls.io/github/uraxy/gaaqoo?branch=master)

Convert images into ones suitable for digital photo frames.
- Scale up/down images.
- Rotate images based on EXIF `Orientation`.
- Overlay shooting datetime (EXIF `DataTimeOriginal`) on each image.

----------

# Install

```shell
$ pip install gaaqoo
```


# Usage

```shell
$ gaaqoo --version
gaaqoo version 0.9.2
$ gaaqoo --help
usage: gaaqoo [-h] [-V] [-f FILE.yml]

Convert images into ones suitable for digital photo frames.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -f FILE.yml, --config FILE.yml
                        config YAML file (default:
                        ~/.config/gaaqoo/default.yml)
$
```


# Config (YAML)

~/.config/gaaqoo/default.yml
(have to create by yourself for now.)

```YAML
# -*- coding: utf-8 -*-

SRC_DIR: ~/Pictures/gaaqoo-src
DST_DIR: ~/Pictures/gaaqoo-dst
SUFFIX: ['.jpg', '.JPG', '.jpeg', '.JPEG']
# exclude if filepath contains there
EXCLUDE: ['_EXCLUDE_', '_NG_']
DST_IMG_SIZE: [800, 480]
FONT: /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
FONT_SIZE: 30
```


# License
MIT License

# Libraries
```shell
$ cat requirements.txt | xargs -n1 yolk -l -f License,Author,Home-page,Summary | egrep -v '^Versions with'
Pillow (3.3.1)
    Summary: Python Imaging Library (Fork)
    Home-page: http://python-pillow.org
    Author: Alex Clark (Fork Author)
    License: Standard PIL License

PyYAML (3.12)
    Summary: YAML parser and emitter for Python
    Home-page: http://pyyaml.org/wiki/PyYAML
    Author: Kirill Simonov
    License: MIT

$
```


----------
# For developers
## example images
- [exif-orientation-examples](https://github.com/recurser/exif-orientation-examples)

## Orientation of image
- `display` (ImageMagick) does not rotate an image regardless of EXIF, so it is suitable for debugging.
- `display -auto-orient` rotates an image based on EXIF.
- `nautilus` (file manager) and `eog` rotate images based on EXIF.

## Show EXIF
- [Exiv2](http://www.exiv2.org/): `exiv2 -pv example.jpg`
