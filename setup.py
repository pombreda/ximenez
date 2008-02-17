import os
from setuptools import setup
from setuptools import find_packages


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
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Intended Audience :: System Administrators',
                 'License :: OSI Approved :: GNU General Public License (GPL)',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: System',
                 'Topic :: Utilities'],
    keywords='collector action plug-in plugin',
    url='http://code.noherring.com/ximenez',
    download_url='http://cheeseshop.python.org/pypi/ximenez',
    )
