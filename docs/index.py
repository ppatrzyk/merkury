from pathlib import Path

README_PATH = Path("README.md")

with README_PATH.open("r") as file:
    readme_md = file.read()

print(readme_md)
#MARKDOWN
