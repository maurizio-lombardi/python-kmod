# Copyright (C) 2012 Red Hat, Inc.
#                    W. Trevor King <wking@tremily.us>
#
# This file is part of python-kmod.
#
# python-kmod is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 2.1 as published
# by the Free Software Foundation.
#
# python-kmod is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python-kmod.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, Extension
from Cython.Build import cythonize
import os
import platform

package_name = 'kmod'

# Read version from kmod/version.py
with open(os.path.join(package_name, 'version.py')) as f:
    exec(f.read())

ext_modules = []
if platform.system() == "Linux":
    # Iterate over .pyx files in the kmod directory and create extensions
    for filename in sorted(os.listdir(package_name)):
        basename, extension = os.path.splitext(filename)
        if extension == '.pyx':
            ext_path = os.path.join(package_name, filename)
            print(f"Compiling {basename} from {ext_path}")
            ext_modules.append(
                Extension(
                    f'{package_name}.{basename}',  # Use kmod.<module_name>
                    [ext_path],  # Path to the .pyx file
                    libraries=['kmod'],  # Link with the kmod library
                )
            )

setup(
    name=package_name,
    version=__version__,
    description='Python binding for kmod',
    packages=[package_name],
    maintainer="Maurizio Lombardi",
    maintainer_email="mlombard@redhat.com",
    ext_modules=cythonize(ext_modules),
    setup_requires=[
        'cython>=0.29',
    ],
    zip_safe=False,  # Disable zip_safe to ensure proper extension loading
)
