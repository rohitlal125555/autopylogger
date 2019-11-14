import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_log_rotate",
    version="2019.11.04",
    author="Rohit Lal",
    author_email="rohitlal.125555@gmail.com",
    description="Python thread-safe logging wrapper module with out of box log rotation facility built for seamless integration in any python script.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://rohitlal.in",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)