try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools import find_packages

setup(
    name='dauto',
    version='0.0.1',
    include_package_data=True,
    packages=find_packages(),
    url='http://192.168.60.60/',
    license='MIT',
    author='yanwh',
    author_email='yanwh@digitalchina.com',
    description='Dauto Core Library For Create GUI',
    long_description=open("README.rst").read(),
    install_requires=[
        'rpyc',
        'pyserial',
        'wxpython'
    ],
    classifiers=[
        "Environment :: GUI Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    platforms='any'
)
