from setuptools import setup, find_packages

# https://setuptools.readthedocs.io/en/latest/setuptools.html#basic-use
setup(
    name='gaaqoo',
    version='0.1.0',
    packages=find_packages(),
    # scripts = ['say_hello.py'],
    install_requires=[
      'Pillow',
    ],

    # metadata for upload to PyPI
    author='uraxy',
    author_email='uraxy123@gmail.com',
    description='Convert images into ones suitable for digital photo frames.',
    license='MIT',
    # keywords=['dummy1', 'dumm2'],
    url='https://github.com/uraxy/gaaqoo',
    # entry_points={
    #     'console_scripts': ['gaaqoo=gaaqoo.command_line:main'],
    # },
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
)
