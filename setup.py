from setuptools import setup, find_packages

setup(
    name='AIO-CodeCheck',  
    version='0.5',  
    packages=find_packages(),
    install_requires=[
        'rich',  
    ],
    entry_points={
        'console_scripts': [
            'aio-check = aio_check.check:main',  
        ],
    },
    author='MOBIN_YM',
    author_email='yaghoobi.m191@gmail.com',  
    description='A simple Python code evaluation tool.',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/mobinym/AIO_CodeCheck',  
    classifiers=[
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],
    python_requires='>=3.6',  
)
