"""
Copyright 2015 BlazeMeter Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import sys

# noinspection PyPackageRequirements
import pip

from setuptools.command.install import install
from setuptools import setup

import bzt


class InstallWithHook(install, object):
    """
    Command adding post-install hook to setup
    """

    def run(self):
        """
        Do the command's job!
        """
        install.run(self)
        self.__hook()

    def __hook(self):
        dirname = bzt.get_configs_dir()
        if os.path.exists(dirname):
            sys.stdout.write("[%s] Found %s\n" % (bzt.VERSION, dirname))
            src = os.path.join(dirname, "10-base.json")
            if os.path.exists(src):
                sys.stdout.write("Removing outdated %s\n" % src)
                os.remove(src)

# thanks to pip there are two incompatible ways to parse requirements.txt
if pip.__version__ < '7':
    requirements = pip.req.parse_requirements('requirements.txt')
else:
    # new versions of pip requires a session
    requirements = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

requires = [str(item.req) for item in requirements]

setup(
    name="bzt",
    version=bzt.VERSION,
    description='Taurus Tool for Continuous Testing',
    author='Andrey Pokhilko',
    author_email='andrey@blazemeter.com',
    url='http://gettaurus.org/',
    download_url='http://gettaurus.org/docs/DeveloperGuide/#Python-Egg-Snapshots',
    license='Apache 2.0',
    platform='any',
    docs_url='http://gettaurus.org/docs/',
    install_requires=requires,
    packages=['bzt', 'bzt.six', 'bzt.jmx', 'bzt.modules', 'bzt.resources'],
    entry_points={
        'console_scripts': [
            'bzt=bzt.cli:main',
            'jmx2yaml=bzt.jmx2yaml:main',
            'soapui2yaml=bzt.soapui2yaml:main',
        ],
    },
    include_package_data=True,
    package_data={
        "bzt": [],
    },
    cmdclass={"install": InstallWithHook}  # TODO: remove it completely once we have most of users upgraded to>=1.8.5
)
