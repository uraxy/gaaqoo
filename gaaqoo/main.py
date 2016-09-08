# -*- coding: utf-8 -*-
import glob
import hashlib
import os
import re
import time
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

# ============================================================
# Config
# ============================================================
SRC_DIR = '/home/uraxy/Pictures/gaaqoo-src'
DST_DIR = '/home/uraxy/Pictures/gaaqoo-dst'
SUFFIX = ('.jpg', '.JPG', '.jpeg', '.JPEG')
EXCLUDE = ('_EXCLUDE_', '_NG_')  # exclude if filepath contains there
DST_IMG_SIZE = (800, 480)
# ============================================================
EXIF_DATETIME_PARSER = re.compile(r'(\d{4}):(\d{2}):(\d{2}) (\d{2}):(\d{2}):(\d{2})')


def get_hash(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    h = hashlib.sha1(data).hexdigest()
    return h[:8]


def print_exif(exif):
    for k, v in exif.items():
        print('  {} (PIL.ExifTags.TAGS[0x{:0>4x}]): {}'.format(PIL.ExifTags.TAGS[k], k, v))


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


def overlay_text(img, text):
    """画像の右下に文字を書きます.

    img自体が変更されます。
    """
    if not text:
        return
    draw = PIL.ImageDraw.Draw(img)
    draw.font = PIL.ImageFont.truetype(
        font='/usr/share/fonts/truetype/msttcorefonts/Verdana_Bold.ttf',
        size=20)
    txt_size = draw.font.getsize(text)  # (width, height)

    x = img.width - txt_size[0] - 5
    y = img.height - txt_size[1] - 5
    draw.text((x, y), text, (255, 255, 255))


def exif_datetime_to_text(exif_datetime):
    """ EXIF形式のDateTimeを、写真にオーバーレイするための文字列に変換します.

    '2016:07:10 17:19:53' => '2016/07/10 17:19'
    """
    x = EXIF_DATETIME_PARSER.match(exif_datetime)
    if x:
        text = '{}/{}/{} {}:{}'.format(x.group(1), x.group(2), x.group(3), x.group(4), x.group(5))
    else:
        text = None
    return(text)


def get_filepaths(dir, suffixes=None, excludes=[]):
    if dir.endswith('/'):
        dir = dir[:-1]
    globed = glob.glob(dir + '/**', recursive=True)

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
    dst_fp = DST_DIR + src_filepath[len(SRC_DIR):]
    dst_fp += '.gaaqoo_{}.jpg'.format(hashcode)
    # dst_fp += '.{}_{}x{}.jpg'.format(hashcode, DST_IMG_SIZE[0], DST_IMG_SIZE[1])
    return dst_fp


def main():
    if not os.path.isdir(SRC_DIR):
        print('SRC_DIR is not a directory: {}'.format(SRC_DIR))
        exit(1)
    src_filepaths = get_filepaths(SRC_DIR, suffixes=SUFFIX, excludes=EXCLUDE)
    if not src_filepaths:
        print('No image file found in SRC_DIR: {}'.format(SRC_DIR))
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

            # resize, rotate
            img.thumbnail(DST_IMG_SIZE, PIL.Image.ANTIALIAS)
            img = transpose(img, ori)
            if dt:
                overlay_text(img, exif_datetime_to_text(dt))

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

    # 変換対象出なかった古いファイルを削除する
    # FIXME **** 何かのエラーがあった時にも、ここで大量のファイルが削除されてしまう！
    dst_filepaths_exists = get_filepaths(DST_DIR)
    for fp in dst_filepaths_exists:
        if fp not in dst_filepaths:
            print('Removing deprecated file: ' + fp)
            os.remove(fp)
    # 空のディレクトリを削除したほうがベター、だけど、まいっか

if __name__ == '__main__':
    main()
