# gaaqoo

[![Build Status](https://travis-ci.org/uraxy/gaaqoo.svg?branch=master)](https://travis-ci.org/uraxy/gaaqoo)
[![Code Health](https://landscape.io/github/uraxy/gaaqoo/master/landscape.svg?style=flat)](https://landscape.io/github/uraxy/gaaqoo/master)
[![Coverage Status](https://coveralls.io/repos/github/uraxy/gaaqoo/badge.svg?branch=master)](https://coveralls.io/github/uraxy/gaaqoo?branch=master)

Convert images into ones suitable for digital photo frames.
- Scale up/down images.
- Rotate images based on EXIF `Orientation`.
- Overlay shooting datetime (EXIF `DataTimeOriginal`) on each image.

----------

# Setup

```shell
$ pip install Pillow  # PIL
$ pip install pyyaml
```

# Config (YAML)

Edit conf/default.yml
```YAML
# -*- coding: utf-8 -*-

SRC_DIR: ~/Pictures/gaaqoo-src
DST_DIR: ~/Pictures/gaaqoo-dst
SUFFIX: ['.jpg', '.JPG', '.jpeg', '.JPEG']
# exclude if filepath contains there
EXCLUDE: ['_EXCLUDE_', '_NG_']
DST_IMG_SIZE: [800, 480]
FONT: /usr/share/fonts/truetype/msttcorefonts/Verdana_Bold.ttf
FONT_SIZE: 30
```

# Run

```shell
$ python -u gaaqoo/convert.py
```
`-u`: unbuffered stdout and stderr


# License
MIT License

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
