import codecs
from setuptools import setup, find_packages

with codecs.open('README.md', encoding='utf-8') as f:
    long_description = f.read();

setup(
    name="exsimple",
    version="1.0.3",
    license='https://github.com/XenoAmess/EXsimple/blob/master/LICENCE',
    description="A public, open, share net-disc.",
    author='XenoAmess',
    author_email='xenoamess@gmail.com',
    url='https://github.com/XenoAmess/EXsimple',
    packages=find_packages(),
    # package_data={
    #     'exsimple': ['README.rst', 'LICENSE']
    # },
    install_requires=[],
    entry_points="""
    [console_scripts]
    exsimple = exsimple.exsimple:main
    """,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    long_description=long_description,
)
