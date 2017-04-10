"""Contains the setup script for the package."""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = dict(

    # meta data
    name='tbont_text_engine',
    version='1.0',

    # package
    package_dir={'': 'lib'},
    packages=['tbont_text_engine',
              'tbont_text_engine.nlp',
              'tbont_text_engine.exceptions',
              'tbont_text_engine.utils',
              'tbont_text_engine.api',
              'tbont_text_engine.vector_space']

)

setup(**config)
