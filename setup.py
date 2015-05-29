import os.path
from setuptools import setup

path = os.path.join(os.path.dirname(__file__), 'README.txt')
with open(path, encoding='utf8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='pgzero',
    version='1.0',
    description="A zero-boilerplate 2D games framework",
    long_description=LONG_DESCRIPTION,
    author='Daniel Pope',
    author_email='mauve@mauveweb.co.uk',
    url='http://pypi.python.org/pypi/pgzero',
    packages=['pgzero'],
    entry_points={
        'console_scripts': [
            'pgzrun = pgzero.runner:main'
        ]
    },
    install_requires=[
        'pygame>=1.9',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
    ]
)
