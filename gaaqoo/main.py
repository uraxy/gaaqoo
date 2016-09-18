# -*- coding: utf-8 -*-
import glob
import hashlib
import os
import re
import time
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import config

EXIF_DATETIME_PARSER = re.compile(config.DATETIME_FORMAT)


def get_hash(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    h = hashlib.sha1(data).hexdigest()
    return h[:8]


def print_exif(exif):
    for k, v in exif.items():
        print('  {} (PIL.ExifTags.TAGS[0x{:0>4x}]): {}'.format(PIL.ExifTags.TAGS[k], k, v))


def _get_contain_size(src_img_size):
    ratio_x = config.DST_IMG_SIZE[0] / src_img_size[0]
    ratio_y = config.DST_IMG_SIZE[1] / src_img_size[1]
    if ratio_x < ratio_y:
        size = (config.DST_IMG_SIZE[0], int(src_img_size[1] * ratio_x))
    else:
        size = (int(src_img_size[0] * ratio_y), config.DST_IMG_SIZE[1])

    return size


def get_exif(img):
    try:
        exif = img._getexif()  # AttributeError
    except AttributeError:
        exif = None
    return exif


def get_datetime_original(exif):
    if not exif:
        return None
    datetime_original = exif.get(0x9003)  # EXIF: DateTimeOriginal
    return datetime_original


def get_orientation(exif):
    if not exif:
        return None
    orientation = exif.get(0x0112)  # EXIF: Orientation
    return orientation


def transpose(src_img, exif_orientation):
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


def _overlay_text(img, text):
    if not text:
        return
    draw = PIL.ImageDraw.Draw(img)
    draw.font = PIL.ImageFont.truetype(
        font=config.FONT,
        size=config.FONT_SIZE)
    txt_size = draw.font.getsize(text)  # (width, height)

    x = img.width - txt_size[0] - 5
    y = img.height - txt_size[1] - 5
    # border
    for xx in range(x-3, x+4):
        for yy in range(y-3, y+4):
            draw.text((xx, yy), text, (0, 0, 0))
    # text
    draw.text((x, y), text, (255, 255, 255))


def exif_datetime_to_text(exif_datetime):
    """ Convert EXIF style DateTime to text for overlay.

    '2016:07:10 17:19:53' => '2016/07/10 17:19'
    """
    x = EXIF_DATETIME_PARSER.match(exif_datetime)
    if x:
        text = '{}/{}/{} {}:{}'.format(x.group(1), x.group(2), x.group(3), x.group(4), x.group(5))
    else:
        text = None
    return(text)


def get_filepaths(dirpath, suffixes=None, excludes=None):
    if excludes is None:
        excludes = []
    if dirpath.endswith('/'):
        dirpath = dirpath[:-1]
    globed = glob.glob(dirpath + '/**', recursive=True)

    filepaths = []
    for fp in globed:
        # photo file?
        if not os.path.isfile(fp):
            continue
        if suffixes and not fp.endswith(suffixes):
            continue
        # exclude?
        skip = False
        for s in excludes:
            if fp.find(s) >= 0:
                skip = True
                break
        if skip:
            continue
        filepaths.append(fp)
    return filepaths


def get_dst_filepath(src_filepath, hashcode):
    dst_fp = config.DST_DIR + src_filepath[len(config.SRC_DIR):]
    dst_fp += '.gaaqoo_{}.jpg'.format(hashcode)
    # dst_fp += '.{}_{}x{}.jpg'.format(hashcode, config.DST_IMG_SIZE[0], config.DST_IMG_SIZE[1])
    return dst_fp


def main():
    if not os.path.isdir(config.SRC_DIR):
        print('config.SRC_DIR is not a directory: {}'.format(config.SRC_DIR))
        exit(1)
    src_filepaths = get_filepaths(config.SRC_DIR, suffixes=config.SUFFIX, excludes=config.EXCLUDE)
    if not src_filepaths:
        print('No image file found in config.SRC_DIR: {}'.format(config.SRC_DIR))
        exit(1)

    dst_filepaths = []
    start_time = time.time()
    for i, fp in enumerate(src_filepaths):
        print('{}/{} [{:.2f}% in {:.3f} sec] {}'.format(i+1, len(src_filepaths), i/len(src_filepaths)*100, time.time() - start_time, fp))

        hashcode = get_hash(fp)
        dst_fp = get_dst_filepath(fp, hashcode)
        dst_filepaths.append(dst_fp)
        if os.path.isfile(dst_fp):
            print('  -> Skip, already exists: ' + dst_fp)
            continue

        try:
            img = PIL.Image.open(fp)

            # EXIF
            exif = get_exif(img)
            ori = get_orientation(exif)
            # print('  Orientation={}'.format(ori))
            if not ori:  # None or 0
                ori = 1
            dt = get_datetime_original(exif)
            # print('  DataTimeOriginal={}'.format(dt))

            # rotate: Must before resizing.
            img = transpose(img, ori)
            # resize: Not thumbnail but scale up/down to keep overlay texts at same scale.
            dst_img_size = _get_contain_size(img.size)
            img = img.resize(dst_img_size, resample=PIL.Image.LANCZOS)

            if dt:
                _overlay_text(img, exif_datetime_to_text(dt))

            # save image
            d = dst_fp.rpartition('/')
            # >>> '/aaa/bbb/cc/dd.jpg'.rpartition('/') ==> ('/aaa/bbb/cc', '/', 'dd.jpg')
            if not os.path.isdir(d[0]):
                os.makedirs(d[0])
            img.save(dst_fp, 'JPEG', quality=95, optimize=True)
        except OSError:
            print("  -> OSError (not image file?): " + fp)
        finally:
            try:
                # when OSError, UnboundLocalError: local variable 'img' referenced before assignment
                img.close()
            except:
                pass

    # delete dst-file which have no src-file
    dst_filepaths_exists = get_filepaths(config.DST_DIR)
    for fp in dst_filepaths_exists:
        if fp not in dst_filepaths:
            print('Removing deprecated file: ' + fp)
            os.remove(fp)
    # removing empty directories is better, but not implemented :-)

if __name__ == '__main__':
    main()
