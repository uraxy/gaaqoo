# gaaqoo

[![PyPI version](https://badge.fury.io/py/gaaqoo.svg)](https://badge.fury.io/py/gaaqoo)
[![Test](https://github.com/uraxy/gaaqoo/actions/workflows/test.yml/badge.svg)](https://github.com/uraxy/gaaqoo/actions/workflows/test.yml)

Convert images into ones suitable for digital photo frames.
- **Reduce file size to save SD card spaces**: Scale down images to fit just to the screen size of your digital photo frame.
- **Ajdust orientation**: Rotate images based on EXIF `Orientation`.
- **Overlay shooting datetime**: Overlay EXIF `DataTimeOriginal`.
- **Convert smart**: Detect new or updated images in src directory recursively, and convert those into dst directory.

'gaaqoo' was named after 'gaku' which means 'frame' in Japanese.

----------

# Install
[![PyPI version](https://badge.fury.io/py/gaaqoo.svg)](https://badge.fury.io/py/gaaqoo)
```shell
$ pip install gaaqoo
```


# Usage

```shell
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
**(have to create by yourself for now.)**

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


# Example
[Nagoya Castle](http://www.nagoyajo.city.nagoya.jp/13_english/index.html) :-)

||image|width x height|orientation|
|:--:|:--:|:--:|:--:|
|**src**|<img width="800px" src="https://github.com/uraxy/uraxy.github.io/blob/master/gaaqoo/examples/src/example01-Orientation-stripped-for-docs.jpg?raw=true"/>|4320x3240|[EXIF] Orientation=6 (Rotate 90 CW)|
|**dst**|<img width="180px" src="https://github.com/uraxy/uraxy.github.io/blob/master/gaaqoo/examples/dst/example01-Orientation-6.jpg.gaaqoo_f6e4f547.jpg?raw=true"/>|360x480 (fits for 800x480)|Horizontal (normal)|


# License
MIT License


# Dependencies
- Pillow (>= 10.0.0)
- PyYAML (>= 6.0)


----------
# For developers

## EXIF orientation example images
- [exif-orientation-examples](https://github.com/recurser/exif-orientation-examples)


## Image rotation based on EXIF orientation when tools show it
Without rotation, so suitable for debugging:
- `display` (ImageMagick)

With rotation:
- `display -auto-orient`
- `nautilus` (file manager)
- `eog`


## EXIF tools
- [ExifTool](http://www.sno.phy.queensu.ca/~phil/exiftool/install.html)
    - `exiftool example.jpg`
- [jhead](http://www.sentex.net/~mwandel/jhead/):
    - `jhead example.jpg`
    - `jhead -autorot example.jpg`
- [Exiv2](http://www.exiv2.org/): `exiv2 -pv example.jpg`

```shell
$ jhead -autorot example.jpg
$ jhead -mkexif example.jpg  # keep DateTimeOriginal. drop GPS, Orientation, and others.
$ exiftool example.jpg
```
