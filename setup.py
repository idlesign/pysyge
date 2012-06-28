import os
from setuptools import setup
from pysyge import VERSION

f = open(os.path.join(os.path.dirname(__file__), 'README'))
readme = f.read()
f.close()

setup(
    name='pysyge',
    version=".".join(map(str, VERSION)),
    description='API to access data from Sypex Geo IP database files from your Python code',
    long_description=readme,
    author="Igor 'idle sign' Starikov",
    author_email='idlesign@yandex.ru',
    url='http://github.com/idlesign/pysyge',
    packages=['pysyge'],
    include_package_data=True,
    install_requires=['setuptools'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
