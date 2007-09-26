import os
from setuptools import setup, find_packages


version_file = 'VERSION.txt'
version = open(version_file).read().strip()
description_file = 'README.txt'
description = open(description_file).read().split('\n\n')[0].strip()
description = description.replace('\n', ' ')
long_description_file = os.path.join('doc', 'README.txt')
long_description = open(long_description_file).read().strip()

setup(
    name='ximenez',
    version=version,
    packages=find_packages('src'),
    namespace_packages=(),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': ('ximenez=ximenez.xim:main', )
        },

    author='Damien Baty',
    author_email='damien.baty@remove-me.gmail.com',
    description=description,
    long_description=long_description,
    license='GNU GPL',
    classifiers=(), ## FIXME
    keywords='FIXME',
    url='', ##FIXME
    download_url='', ## FIXME
    )
