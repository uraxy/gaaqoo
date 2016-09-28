from setuptools import setup, find_packages
from gaaqoo import __version__, __description__

# https://setuptools.readthedocs.io/en/latest/setuptools.html#basic-use
setup(
    name='gaaqoo',
    version=__version__,
    packages=find_packages(),
    # scripts = ['say_hello.py'],
    install_requires=[
      'Pillow',
      'PyYAML',
    ],

    # http://doc.pytest.org/en/latest/goodpractices.html#integrating-with-setuptools-python-setup-py-test-pytest-runner
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    # metadata for upload to PyPI
    author='uraxy',
    author_email='uraxy123@gmail.com',
    description=__description__,
    license='MIT',
    # keywords=['dummy1', 'dumm2'],
    url='https://github.com/uraxy/gaaqoo',
    entry_points={
        'console_scripts': ['gaaqoo=gaaqoo.command_line:main'],
    },
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Utilities',
    ],
)
