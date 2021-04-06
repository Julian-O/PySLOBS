import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PySLOBS",
    version="1.2.0",
    author="Julian-O",
    # author_email="",
    description="Python wrapper to StreamLabs OBS API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Julian-O/pyslobs",
    packages=setuptools.find_packages(),
    tests_require=[],
    install_requires=["websocket_client"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.9",
)
