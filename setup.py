from setuptools import setup


setup(
    name='pgzero',
    version='0.1',
    author='Daniel Pope',
    author_email='mauve@mauveweb.co.uk',
    url='http://pypi.python.org/pypi/pgzero',
    packages=['pgzero'],
    entry_points={
        'console_scripts': [
            'pgzrun = pgzero.runner:main'
        ]
    }
)
