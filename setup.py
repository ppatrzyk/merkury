from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='merkury',
    version='0.1',
    license='MIT',
    description='TODO',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    author='Piotr Patrzyk',
    url='https://github.com/ppatrzyk/merkury',
    packages=['merkury'],
    python_requires='>=3.10',
    install_requires=[
        'docopt>=0.6.2',
        'Jinja2>=3.1.2',
    ],
    entry_points={
        'console_scripts': [
            'merkury=merkury.main:main',
        ],
    },
)