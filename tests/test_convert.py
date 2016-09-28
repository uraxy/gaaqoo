# -*- coding: utf-8 -*-
"""Test for convert.py."""
import unittest
import PIL.Image
import gaaqoo.convert


class TestConvert(unittest.TestCase):
    """Test for convert.py."""

    @classmethod
    def setUpClass(cls):
        pass
        # print()
        # print('> setUpClass method is called.')

    @classmethod
    def tearDownClass(cls):
        pass
        # print()
        # print('> tearDownClass method is called.')

    def setUp(self):
        pass
        # print()
        # print('>> setUp method is called.')

    def tearDown(self):
        pass
        # print()
        # print('>> tearDown method is called.')

    def test__get_contain_size__src_x_eq_dst_x_src_y_eq_dst_y(self):
        src_img_size = (800, 480)  # tupple
        dst_img_size = (800, 480)
        expected = (800, 480)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(actual, expected)

    def test__get_contain_size__src_x_lt_dst_x_src_y_eq_dst_y(self):
        src_img_size = [800/2, 480]
        dst_img_size = (800, 480)
        expected = (400, 480)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(actual, expected)

    def test__get_contain_size__src_x_gt_dst_x_src_y_eq_dst_y(self):
        src_img_size = [800*2, 480]
        dst_img_size = (800, 480)
        expected = (800, 240)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(actual, expected)

    def test__get_contain_size__src_x_eq_dst_x_src_y_lt_dst_y(self):
        src_img_size = [800, 480/2]
        dst_img_size = (800, 480)
        expected = (800, 240)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(actual, expected)

    def test__get_contain_size__src_x_lt_dst_x_src_y_gt_dst_y(self):
        src_img_size = [800, 480*2]
        dst_img_size = (800, 480)
        expected = (400, 480)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(actual, expected)

    def test__get_contain_size__ratio_gt_gt_ratio_y(self):
        src_img_size = [800*2, 480*4]
        dst_img_size = (800, 480)
        expected = (400, 480)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(actual, expected)

    def test__get_contain_size__ratio_x_lt_ratio_y(self):
        src_img_size = [800*3, 480*2]
        dst_img_size = (800, 480)
        expected = (800, 320)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(actual, expected)

    def test__get_contain_size__upscale_ratio_x_lt_ratio_y(self):
        src_img_size = [800/2, 480/4]
        dst_img_size = (800, 480)
        expected = (800, 240)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(actual, expected)

    def test__exif_datetime_to_text(self):
        exif_datetime = '2016:07:10 17:19:53'
        expected = '2016/07/10 17:19'
        actual = gaaqoo.convert._exif_datetime_to_text(exif_datetime)
        self.assertEqual(actual, expected)

    def test__exif_datetime_to_text__empty(self):
        exif_datetime = ''
        expected = ''
        actual = gaaqoo.convert._exif_datetime_to_text(exif_datetime)
        self.assertEqual(actual, expected)

    def test__hash(self):
        filepath = './tests/images/IMG_20150301_121137.jpg'
        expected = '4145e0a5'
        actual = gaaqoo.convert._hash(filepath)
        self.assertEqual(actual, expected)

    def test__get_dst_filepath__1(self):
        src_dir = './tests'  # not endwith('/')
        dst_dir = '/tmp/'  # endswith('/')
        src_filepath = './tests/images/IMG_20150301_121137.jpg'
        expected = '/tmp/images/IMG_20150301_121137.jpg.gaaqoo_4145e0a5.jpg'
        actual = gaaqoo.convert._get_dst_filepath(src_dir, dst_dir, src_filepath)
        self.assertEqual(actual, expected)

    def test__get_dst_filepath__2(self):
        src_dir = './tests/'  # endwith('/')
        dst_dir = '/tmp'  # not endswith('/')
        src_filepath = './tests/images/IMG_20150301_121137.jpg'
        expected = '/tmp/images/IMG_20150301_121137.jpg.gaaqoo_4145e0a5.jpg'
        actual = gaaqoo.convert._get_dst_filepath(src_dir, dst_dir, src_filepath)
        self.assertEqual(actual, expected)

    def test__get_filepaths(self):
        dirpath = './tests'
        suffixes = ('.jpg', '.JPG')
        excludes = ('_EXCLUDE_', '_DUMMY_')
        expected = ['./tests/images/IMG_20150301_121137.jpg']
        actual = gaaqoo.convert._get_filepaths(dirpath, suffixes, excludes)
        self.assertEqual(actual, expected)

    def test__get_filepaths__suffixes_1_tuple(self):
        dirpath = './tests'
        suffixes = ('.dummy')
        excludes = ('_EXCLUDE_', '_DUMMY_')
        expected = []
        actual = gaaqoo.convert._get_filepaths(dirpath, suffixes, excludes)
        self.assertEqual(actual, expected)

    def test__get_filepaths__suffixes_1_list(self):
        dirpath = './tests'
        suffixes = ['.dummy']
        excludes = ('_EXCLUDE_', '_DUMMY_')
        expected = []
        actual = gaaqoo.convert._get_filepaths(dirpath, suffixes, excludes)
        self.assertEqual(actual, expected)

    def test__get_filepaths__suffixes2(self):
        dirpath = './tests'
        suffixes = ('dummy', 'dummy2')
        excludes = ('_EXCLUDE_', '_DUMMY_')
        expected = []
        actual = gaaqoo.convert._get_filepaths(dirpath, suffixes, excludes)
        self.assertEqual(actual, expected)

    def test__get_filepaths__excludes(self):
        dirpath = './tests'
        suffixes = ('jpg', 'JPG')
        excludes = ('images')
        expected = []
        actual = gaaqoo.convert._get_filepaths(dirpath, suffixes, excludes)
        self.assertEqual(actual, expected)

    def test__get_filepaths__without_suffixes_and_excludes(self):
        dirpath = './tests'
        expected = ['./tests/images/IMG_20150301_121137.jpg']
        actual = gaaqoo.convert._get_filepaths(dirpath)
        self.assertEqual(actual, expected)

    def test__get_exif(self):
        # expected = None
        with PIL.Image.open('./tests/images/IMG_20150301_121137.jpg', 'r') as img:
            actual = gaaqoo.convert._get_exif(img)
        # self.assertEqual(actual, expected)  # Nothing

    def test__get_datetime_original(self):
        expected = '2015:03:01 12:11:38'
        with PIL.Image.open('./tests/images/IMG_20150301_121137.jpg', 'r') as img:
            exif = gaaqoo.convert._get_exif(img)
        actual = gaaqoo.convert._get_datetime_original(exif)
        self.assertEqual(actual, expected)

    def test__get_datetime_original__exif_none(self):
        exif = None
        expected = None
        actual = gaaqoo.convert._get_datetime_original(exif)
        self.assertEqual(actual, expected)

    def test__get_orientation(self):
        expected = 1
        with PIL.Image.open('./tests/images/IMG_20150301_121137.jpg', 'r') as img:
            exif = gaaqoo.convert._get_exif(img)
        actual = gaaqoo.convert._get_orientation(exif)
        self.assertEqual(actual, expected)

    def test__get_orientation__exif_none(self):
        exif = None
        expected = None
        actual = gaaqoo.convert._get_orientation(exif)
        self.assertEqual(actual, expected)

    def test__overlay_text__text_none(self):
        text = None
        expected = None
        with PIL.Image.open('./tests/images/IMG_20150301_121137.jpg', 'r') as img:
            actual = gaaqoo.convert._overlay_text(img, text)
        self.assertEqual(actual, expected)  # always None
