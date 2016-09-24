# -*- coding: utf-8 -*-
"""Test for convert.py."""
import unittest
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
        self.assertEqual(expected, actual)

    def test__get_contain_size__src_x_lt_dst_x_src_y_eq_dst_y(self):
        src_img_size = [800/2, 480]
        dst_img_size = (800, 480)
        expected = (400, 480)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(expected, actual)

    def test__get_contain_size__src_x_gt_dst_x_src_y_eq_dst_y(self):
        src_img_size = [800*2, 480]
        dst_img_size = (800, 480)
        expected = (800, 240)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(expected, actual)

    def test__get_contain_size__src_x_eq_dst_x_src_y_lt_dst_y(self):
        src_img_size = [800, 480/2]
        dst_img_size = (800, 480)
        expected = (800, 240)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(expected, actual)

    def test__get_contain_size__src_x_lt_dst_x_src_y_gt_dst_y(self):
        src_img_size = [800, 480*2]
        dst_img_size = (800, 480)
        expected = (400, 480)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(expected, actual)

    def test__get_contain_size__ratio_gt_gt_ratio_y(self):
        src_img_size = [800*2, 480*4]
        dst_img_size = (800, 480)
        expected = (400, 480)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(expected, actual)

    def test__get_contain_size__ratio_x_lt_ratio_y(self):
        src_img_size = [800*3, 480*2]
        dst_img_size = (800, 480)
        expected = (800, 320)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(expected, actual)

    def test__get_contain_size__upscale_ratio_x_lt_ratio_y(self):
        src_img_size = [800/2, 480/4]
        dst_img_size = (800, 480)
        expected = (800, 240)
        actual = gaaqoo.convert._get_contain_size(src_img_size, dst_img_size)
        self.assertEqual(expected, actual)

    def test__exif_datetime_to_text(self):
        exif_datetime = '2016:07:10 17:19:53'
        expected = '2016/07/10 17:19'
        actual = gaaqoo.convert._exif_datetime_to_text(exif_datetime)
        self.assertEqual(expected, actual)

    def test__exif_datetime_to_text__empty(self):
        exif_datetime = ''
        expected = ''
        actual = gaaqoo.convert._exif_datetime_to_text(exif_datetime)
        self.assertEqual(expected, actual)

    def test__hash(self):
        filepath = '/dev/null'
        expected = 'da39a3ee'
        actual = gaaqoo.convert._hash(filepath)
        self.assertEqual(expected, actual)

    def test__get_dst_filepath(self):
        src_dir = '/dev'  # not endwith('/')
        dst_dir = '/tmp/'  # endswith('/')
        src_filepath = '/dev/null'
        expected = '/tmp/null.gaaqoo_da39a3ee.jpg'
        actual = gaaqoo.convert._get_dst_filepath(src_dir, dst_dir, src_filepath)
        self.assertEqual(expected, actual)

    def test__get_filepaths(self):
        dirpath = '/dev'
        suffixes = ('null', 'zero')
        excludes = ('_EXCLUDE_', '_DUMMY_')
        expected = []
        actual = gaaqoo.convert._get_filepaths(dirpath, suffixes, excludes)
        self.assertEqual(expected, actual)

    def test__get_filepaths__without_suffixes_and_excludes(self):
        dirpath = '/dev'
        expected = []
        actual = gaaqoo.convert._get_filepaths(dirpath)
        self.assertEqual(expected, actual)
