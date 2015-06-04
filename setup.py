import sys
import os.path
from setuptools import setup

path = os.path.join(os.path.dirname(__file__), 'README.txt')
with open(path, encoding='utf8') as f:
    LONG_DESCRIPTION = f.read()

install_requires = ['pygame>=1.9']
if sys.version < (3, 4):
    install_requires.append("enum34")
    
setup(
    name='pgzero',
    version='1.0.1',
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
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
    ]
)
