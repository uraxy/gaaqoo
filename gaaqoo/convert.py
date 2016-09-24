# -*- coding: utf-8 -*-
"""Convert image files."""
import glob
import hashlib
import os
import re
import time
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
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
            config = yaml.load(f)
        except yaml.YAMLError as e:  # FIXME
            print(e)  # FIXME
            raise e
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


def _get_orientation(exif):
    """Get Orientation from EXIF.

    Args:
        exif (dict):

    Returns:
        int or None: Orientation
    """
    if not exif:
        return None
    orientation = exif.get(0x0112)  # EXIF: Orientation
    return orientation


def _transpose(src_img, exif_orientation):
    """Rotate image by EXIF Orientation.

    Args:
        src_img (PIL.Image):
        exif_orientation (int):

    Returns:
        PIL.Image: Rotated image
    """
    convert_image = {
        1: lambda img: img,
        2: lambda img: img.transpose(PIL.Image.FLIP_LEFT_RIGHT),
        3: lambda img: img.transpose(PIL.Image.ROTATE_180),
        4: lambda img: img.transpose(PIL.Image.FLIP_TOP_BOTTOM),
        5: lambda img: img.transpose(PIL.Image.FLIP_LEFT_RIGHT).transpose(PIL.Image.ROTATE_90),
        6: lambda img: img.transpose(PIL.Image.ROTATE_270),
        7: lambda img: img.transpose(PIL.Image.FLIP_LEFT_RIGHT).transpose(PIL.Image.ROTATE_270),
        8: lambda img: img.transpose(PIL.Image.ROTATE_90),
    }
    dst_img = convert_image[exif_orientation](src_img)
    return dst_img


def _overlay_text(
        img,
        text,
        font='/usr/share/fonts/truetype/msttcorefonts/Verdana_Bold.ttf',
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
        return
    draw = PIL.ImageDraw.Draw(img)
    draw.font = PIL.ImageFont.truetype(
        font=font,
        size=font_size)
    txt_size = draw.font.getsize(text)  # (width, height)

    x = img.width - txt_size[0] - 5
    y = img.height - txt_size[1] - 5
    # border
    for xx in range(x-3, x+4):
        for yy in range(y-3, y+4):
            draw.text((xx, yy), text, (0, 0, 0))
    # text
    draw.text((x, y), text, (255, 255, 255))


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


def _get_filepaths(dirpath, suffixes=None, excludes=None):
    """find filepaths which meet conditions (suffixes and excludes).

    Args:
        dirpath (str): Path of top directory
        suffixes (list of str or tuple of str): Suffixes of files to get
        excludes (list of str or tuple of str): Exclude files which contains one of this in filepath

    Returns:
        list of str: filepaths
    """
    suffixes = tuple(suffixes) if suffixes else ()
    if excludes is None:
        excludes = ()
    if not dirpath.endswith('/'):
        dirpath = dirpath + '/'

    globed = glob.glob(dirpath + '**', recursive=True)  # >= Python 3.5
    filepaths = []
    for fp in globed:
        # photo file?
        if not os.path.isfile(fp):
            continue
        if suffixes and not fp.endswith(suffixes):
            continue
        # exclude?
        skip = False
        for s in excludes:  # TODO must ignore leading SRC_DIR part.
            if fp.find(s) >= 0:
                skip = True
                break
        if skip:
            continue
        filepaths.append(fp)
    return filepaths


def _hash(filepath):
    """Hash str (len=8) of file.

    Args:
        filepath (str): filepath to get hash.

    Returns:
        str: Hash
    """
    with open(filepath, 'rb') as f:
        data = f.read()
    h = hashlib.sha1(data).hexdigest()
    return h[:8]


def _get_dst_filepath(src_dir, dst_dir, src_filepath):
    """Get dst filepath.

    Args:
        src_dir (str):
        dst_DIR (str):
        src_filepath (str):

    Returns:
        str: filepath
    """

    if not src_dir.endswith('/'):
        src_dir += '/'
    if not dst_dir.endswith('/'):
        dst_dir += '/'

    hashcode = _hash(src_filepath)
    dst_fp = dst_dir + src_filepath[len(src_dir):]
    dst_fp += '.gaaqoo_{}.jpg'.format(hashcode)
    return dst_fp


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
            ori = _get_orientation(exif)
            # print('  Orientation={}'.format(ori))
            if not ori:  # None or 0
                ori = 1
            dt = _get_datetime_original(exif)
            # print('  DataTimeOriginal={}'.format(dt))

            # rotate: Must before resizing.
            img = _transpose(img, ori)
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

if __name__ == '__main__':
    main()
