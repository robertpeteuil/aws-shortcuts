try:
    from setuptools import setup
except ImportError:
    raise ImportError(
        "setuptools module required, please go to "
        "https://pypi.python.org/pypi/setuptools and follow the instructions "
        "for installing setuptools"
    )
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='awss',
    packages=['awss'],
    entry_points={'console_scripts': ['awss=awss.core:main']},
    version='0.9.13',
    author="Robert Peteuil",
    author_email="robert.s.peteuil@gmail.com",
    url='https://github.com/robertpeteuil/aws-shortcuts',
    download_url='https://pypi.python.org/pypi/awss/',
    license='GNU General Public License v3 (GPLv3)',
    description='AWS Shortcuts for Command-Line Instance Control',
    platforms='any',
    keywords='AWS EC2 instance control ssh',
    install_requires=['boto3>=1.4',
                      'future>=0.14',
                      'colorama'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration'],
    long_description=long_description

)
