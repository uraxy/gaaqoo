# gaaqoo

Convert images into ones suitable for digital photo frames.
- Reduce images.
- Rotate images based on EXIF `Orientation`.
- Overlay shooting date and time (EXIF `DataTimeOriginal`) on each image.

----------

# Setup

```shell
$ pip install Pillow  # PIL
```

# Config

Edit gaaqoo/main.py.
```python
# ============================================================
# Config
# ============================================================
SRC_DIR = '/home/uraxy/Pictures/gaaqoo-src'  # symlink in my case,
DST_DIR = '/home/uraxy/Pictures/gaaqoo-dst'  # symlink in my case,
SUFFIX = ('.jpg', '.JPG', '.jpeg', '.JPEG')  # target image files' suffix
EXCLUDE = ('_EXCLUDE_', '_NG_')  # exclude if filepath contains there
DST_IMG_SIZE = (800, 480)
# ============================================================
```

# Run

```shell
$ python -u gaaqoo/main.py
```
`-u`: unbuffered stdout and stderr


# License
MIT License

----------
# For developers
## Rotation of images.
- `display` (ImageMagick) does not rotate an image regardless of EXIF, so it is suitable for debugging.
- `display -auto-orient` rotates an image based on EXIF.
- `nautilus` (file manager) and `eog` rotate an image based on EXIF.
