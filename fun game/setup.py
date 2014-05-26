"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['Ha_Hugo_game.py']
DATA_FILES = ['alien.png','big_heart.png','dead_ha.png','glove.png','ha.png','heart.png','hugo.png','stunned_ha.png','stunned_hugo.png', 'won_hugo.png']
OPTIONS = {'argv_emulation': True}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)