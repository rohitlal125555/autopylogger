import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autopylogger",
    packages = ['autopylogger'], 
    version="1.0",
    license='MIT',
    description="Wrapper module for logging with out of box log rotation and critical errors mailing feature",
    author="Rohit Lal @rohitlal125555",
    author_email="rohitlal125555@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohitlal125555/autopylogger/",
    keywords = ['logging', 'autologging', 'pyautologging', 'python logger', 'log rotate', 'log rotation', 'log mailing'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
