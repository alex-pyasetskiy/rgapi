import os.path

from setuptools import setup

__version__ = '0.0.1'

_description = os.path.join(os.path.dirname(__file__), 'README.md')

setup(
    name='RGApi',
    version=__version__,
    packages=['rgapi'],
    description='Full-featured Riot Game API python client.',
    long_description=open(_description).read(),
    author='Alex Pyasetskiy',
    url='TBD',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Text Processing',
        'Topic :: Games/Entertainment :: Role-Playing',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP'
    ],
    license='MIT',
    install_requires=[
        'requests==2.8.1',
        'enum==0.4.6',
        'pytz'
    ],
 )
