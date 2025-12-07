import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PySLOBS",
    # If you want to bump the version, consider also bumping the
    # 'tested on' versions in the README.md.
    version="2.0.6",
    author="Julian-O",
    # author_email="",
    description="Python wrapper to StreamLabs Desktop API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Julian-O/pyslobs",
    packages=setuptools.find_packages(),
    install_requires=["websocket-client"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.10",
)
