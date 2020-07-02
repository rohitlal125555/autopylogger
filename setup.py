import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autopylogger",
    version="1.0",
    author="Rohit Lal @rohitlal125555",
    author_email="rohitlal125555@gmail.com",
    description="Wrapper module for logging with out of box log rotation and mailing feature",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohitlal125555/autopylogger/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU GENERAL PUBLIC LICENSE",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.3',
)
