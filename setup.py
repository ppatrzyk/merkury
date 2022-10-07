from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name="merkury",
    version="0.4",
    license="MIT",
    description="Turn Python scripts into HTML reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    author="Piotr Patrzyk",
    url="https://github.com/ppatrzyk/merkury",
    packages=["merkury"],
    package_data={"merkury": ["templates/*", "templates/assets/*"]},
    python_requires=">=3.10",
    install_requires=[
        "docopt>=0.6.2",
        "Jinja2>=3.1.2",
        "Markdown>=3.4.1",
        "pdfkit>=1.0.0",
        "psycopg>=3.1.3",
        "psycopg-binary>=3.1.3",
        "prettytable>=3.4.1",
        "sqlparse>=0.4.3",
    ],
    entry_points={
        "console_scripts": [
            "merkury=merkury.main:main",
        ],
    },
)
