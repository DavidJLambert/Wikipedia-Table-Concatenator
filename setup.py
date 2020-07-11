""" setup.py
REPOSITORY:
  https://github.com/DavidJLambert/Wikipedia-Table-Contactenator

SUMMARY:
  Copies Wikipedia page, but with tables "joined" (as in SQL "join").

VERSION:
  0.1.1

AUTHOR:
  David J. Lambert

DATE:
  July 10, 2020
"""

from distutils.core import setup

with open("README.rst", 'r') as f:
    long_description = f.read()

setup(
    author='David J. Lambert',
    author_email='David5Lambert7@gmail.com',
    description='Downloads crossword puzzle pdfs from www.puzzlesociety.com',
    license='MIT License',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    name='beautifulSoup',
    url='https://github.com/DavidJLambert/Wikipedia-Table-Contactenator',
    version='0.1.1',
    install_requires=[
          'beautifulsoup4',
          'lxml',
          'requests',
    ],
    py_modules=["Wikipedia-Table-Contactenator"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ],
)
