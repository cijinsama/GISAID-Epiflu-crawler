from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name="Crawler_GISAID",
    version="0.2",
    author="yiliu",
    author_email="yil349@ucsd.edu",
    packages=find_packages("src"),
    package_data={"": ['*.txt', '*.zip', '*.csv', '*.model']},
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "crawler = Crawler_GISAID.cli:main",
        ],
    },
    python_requires='>=3.8.18, <3.11',
    install_requires=REQUIREMENTS
)
