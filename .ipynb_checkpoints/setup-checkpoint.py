import os
import sys
from setuptools import find_packages
from distutils.core import setup

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup
    from distutils.cmd import Command

import versioneer

from setuptools.extension import Extension

ext_modules = [Extension("quickle", ["quickle.c"])]


packages = find_packages()
#packages.remove('bolt4ds.sparsity.test')

here = os.path.abspath(os.path.dirname(__file__))

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
with open("README.md", "r") as fh:
    long_description = fh.read()

about = {}
with open(os.path.join(here, 'bolt4ds', '__version__.py'), 'r') as f:
    exec(f.read(), about)

class VerifyVersionCommand(Command):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != about['__version__']:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, about['__version__']
            )
            sys.exit(info)
class TagReleaseCommand(Command):
    """Custom command to use the version from __version__.py to tag a release"""
    description = 'verify that the git tag matches our version'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('git tag %s' % about['__version__'])

setup(
    name='bolt4ds',
    #version=versioneer.get_version(),
    version=about['__version__'],
    author='leepand',
    author_email='pandeng.li@163.com',
    description="data science processing toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leepand/bolt4ds",
    packages=packages,
    #ext_modules=ext_modules,
    include_package_data = True,
    #cmdclass=versioneer.get_cmdclass(),
    install_requires=requirements,
    extras_require={
        'dask': ['toolz','dask[dataframe]'],
        'pipe': ['d6tpipe', 'jinja2']},
    test_requires=[
        'boto3==1.7.84',
        'botocore==1.10.84',
        'moto==1.3.6'
    ],
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'verify': VerifyVersionCommand,
        'tag_release': TagReleaseCommand
    }
)

