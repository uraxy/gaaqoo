# -*- coding: utf-8 -*-
"""Convert image files."""
import hashlib
import os
import re
import time
from pathlib import Path

import PIL.ExifTags
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import PIL.ImageOps
import yaml






def _read_config(yaml_filepath):
    """Read config from YAML file.

    Args:
        yaml_filepath (str):

    Returns:
        dict: Config
    """
    with open(yaml_filepath, 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise RuntimeError(f"Failed to parse config: {e}") from e

    config['SRC_DIR_ORG'] = config['SRC_DIR']
    config['SRC_DIR'] = os.path.expandvars(os.path.expanduser(config['SRC_DIR']))
    if not config['SRC_DIR'].endswith('/'):
        config['SRC_DIR'] = config['SRC_DIR'] + '/'

    config['DST_DIR_ORG'] = config['DST_DIR']
    config['DST_DIR'] = os.path.expandvars(os.path.expanduser(config['DST_DIR']))
    if not config['DST_DIR'].endswith('/'):
        config['DST_DIR'] = config['DST_DIR'] + '/'
    return config


def _print_exif(exif):
    """Pretty print of exif.

    Args:
        exif (dict): EXIF got with _get_exif()
    """
    for k, v in exif.items():
        print('  {} (PIL.ExifTags.TAGS[0x{:0>4x}]): {}'.format(PIL.ExifTags.TAGS[k], k, v))


def _get_contain_size(src_img_size, dst_img_size):
    """Get image size which fit `dst_img_size`.

    Args:
        src_img_size (int, int): (x, y)
        dst_img_size (int, int): (x, y)

    Returns:
        (int, int): (x, y)
    """
    ratio_x = dst_img_size[0] / src_img_size[0]
    ratio_y = dst_img_size[1] / src_img_size[1]
    if ratio_x < ratio_y:
        size = (dst_img_size[0], int(src_img_size[1] * ratio_x))
    else:
        size = (int(src_img_size[0] * ratio_y), dst_img_size[1])

    return size


def _get_exif(img):
    """Get EXIF from PIL.Image.

    Args:
        img (PIL.Image):

    Returns:
        dict: EXIF
    """
    try:
        exif = img._getexif()  # AttributeError
    except AttributeError:
        exif = None
    return exif


def _get_datetime_original(exif):
    """Get DateTimeOriginal from EXIF.

    Args:
        exif (dict):

    Returns:
        str: DateTimeOriginal
    """
    if not exif:
        return None
    datetime_original = exif.get(0x9003)  # EXIF: DateTimeOriginal
    return datetime_original





def _overlay_text(
        img,
        text,
        font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        font_size=30):
    """Overlay text on `Image`.

    Args:
        img (PIL.Image): Image, on which text is going to overlayed in place
        text (str): text to overlay
        font (str): font filepath
        font_size (int): font size

    Returns:
        None:
    """
    if not text:
        return None
    draw = PIL.ImageDraw.Draw(img)
    draw.font = PIL.ImageFont.truetype(
        font=font,
        size=font_size)
    
    bbox = draw.textbbox((0, 0), text, font=draw.font)
    txt_width = bbox[2] - bbox[0]
    txt_height = bbox[3] - bbox[1]

    x = img.width - txt_width - 5
    y = img.height - txt_height - 5
    # border
    for xx in range(x-3, x+4):
        for yy in range(y-3, y+4):
            draw.text((xx, yy), text, (0, 0, 0))
    # text
    draw.text((x, y), text, (255, 255, 255))
    return None


_EXIF_DATETIME_PARSER = re.compile(r'(\d{4}):(\d{2}):(\d{2}) (\d{2}):(\d{2}):(\d{2})')


def _exif_datetime_to_text(exif_datetime):
    """Convert EXIF style DateTime to text for overlay.

    Args:
        exif_datetime (str): e.g. '2016:07:10 17:19:53'

    Returns:
        string: e.g. '2016/07/10 17:19'. Seconds is ignored.
    """
    x = _EXIF_DATETIME_PARSER.match(exif_datetime)
    if x:
        text = '{}/{}/{} {}:{}'.format(x.group(1), x.group(2), x.group(3), x.group(4), x.group(5))
    else:
        text = ''
    return(text)


def _get_filepaths(
        dirpath,
        suffixes=('.jpg', '.JPG', '.jpeg', '.JPEG'),
        excludes=None):
    """find filepaths which meet conditions (suffixes and excludes).

    Args:
        dirpath (str): Path of top directory
        suffixes (list of str or tuple of str): Suffixes of files to get
        excludes (list of str or tuple of str): Exclude files which contains one of this in filepath

    Returns:
        list of str: filepaths
    """
    if isinstance(suffixes, list):
        suffixes = tuple(suffixes)
    if excludes is None:
        excludes = ()
    
    p_dir = Path(os.path.expandvars(dirpath)) # Ensure env vars are expanded before check
    if not p_dir.is_dir():
        return []

    filepaths = []
    # recursive search
    for p in p_dir.rglob('*'):
        if not p.is_file():
            continue
        if suffixes and not p.name.endswith(suffixes):
            continue
        
        fp_str = str(p)
        skip = False
        for s in excludes: 
            if s in fp_str:
                skip = True
                break
        if skip:
            continue
        filepaths.append(fp_str)
    return filepaths


def _hash(filepath):
    """Hash str (len=8) of file.

    Args:
        filepath (str): filepath to get hash.

    Returns:
        str: Hash
    """
    h = hashlib.sha1()
    chunk_size = 4096
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()[:8]


def _get_dst_filepath(src_dir, dst_dir, src_filepath):
    """Get dst filepath.

    Args:
        src_dir (str):
        dst_dir (str):
        src_filepath (str):

    Returns:
        str: filepath
    """
    hashcode = _hash(src_filepath)
    
    p_src = Path(src_filepath)
    p_src_dir = Path(src_dir)
    p_dst_dir = Path(dst_dir)
    
    try:
        rel = p_src.relative_to(p_src_dir)
    except ValueError:
        # Fallback for when strings don't perfectly match but should be relative
        # e.g. /tmp/a vs /tmp/a/
        # resolve() might help but might be slow or follow symlinks. 
        # We try simple string fallback if relative_to fails, attempting to mimic old behavior safely
        if str(src_filepath).startswith(str(src_dir).rstrip(os.sep)):
             rel = str(src_filepath)[len(str(src_dir).rstrip(os.sep)):]
             if rel.startswith(os.sep): 
                 rel = rel[1:]
             rel = Path(rel)
        else:
             raise

    dst_fp = p_dst_dir / rel
    # Match existing suffix appending behavior: filename.jpg -> filename.jpg.gaaqoo_HASH.jpg
    # The existing code did: dst_fp += '.gaaqoo_....jpg'
    return f"{dst_fp}.gaaqoo_{hashcode}.jpg"


def main(conf_yaml_file):
    """Main.

    Args:
        conf_yaml_file (str): File path of config YAML file
    Returns:
        None:
    """
    conf = _read_config(conf_yaml_file)

    if not os.path.isdir(conf['SRC_DIR']):
        print('SRC_DIR is not a directory: {}'.format(conf['SRC_DIR_ORG']))
        exit(1)
    src_filepaths = _get_filepaths(
        conf['SRC_DIR'],
        suffixes=conf['SUFFIX'],
        excludes=conf['EXCLUDE'])
    if not src_filepaths:
        print('No image file found in SRC_DIR: {}'.format(conf['SRC_DIR']))
        exit(1)

    dst_filepaths = []
    start_time = time.time()
    for i, fp in enumerate(src_filepaths):
        print('{}/{} [{:.2f}% in {:.3f} sec] {}'.format(
            i+1,
            len(src_filepaths),
            i/len(src_filepaths)*100,
            time.time()-start_time,
            fp))

        dst_fp = _get_dst_filepath(conf['SRC_DIR'], conf['DST_DIR'], fp)
        dst_filepaths.append(dst_fp)
        if os.path.isfile(dst_fp):
            print('  -> Skip, already exists: ' + dst_fp)
            continue

        with PIL.Image.open(fp) as img:
            # EXIF
            exif = _get_exif(img)
            dt = _get_datetime_original(exif)

            # rotate: Must before resizing.
            img = PIL.ImageOps.exif_transpose(img)
            # resize: Not thumbnail but scale up/down to keep overlay texts at same scale.
            dst_img_size = _get_contain_size(img.size, conf['DST_IMG_SIZE'])
            img = img.resize(dst_img_size, resample=PIL.Image.LANCZOS)

            if dt:
                _overlay_text(img, _exif_datetime_to_text(dt), conf['FONT'], conf['FONT_SIZE'])

            # save image
            d = dst_fp.rpartition('/')
            # >>> '/aaa/bbb/cc/dd.jpg'.rpartition('/') ==> ('/aaa/bbb/cc', '/', 'dd.jpg')
            if not os.path.isdir(d[0]):
                os.makedirs(d[0])
            img.save(dst_fp, 'JPEG', quality=95, optimize=True)
        # except OSError:
        #     print("  -> OSError (not image file?): " + fp)

    # delete dst-file which have no src-file
    dst_filepaths_exists = _get_filepaths(conf['DST_DIR'])
    for fp in dst_filepaths_exists:
        if fp not in dst_filepaths:
            print('Removing deprecated file: ' + fp)
            os.remove(fp)
    # removing empty directories is better, but not implemented :-)
