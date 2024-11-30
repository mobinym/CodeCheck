from setuptools import setup, find_packages

setup(
    name='AIO-CodeCheck',  
    version='0.2',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'aio-check = aio_check.check:main',  
        ],
    },
    author='MOBIN_YM',
    description='A package to evaluate Python code submissions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mobinym/AIO_CHECK',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
