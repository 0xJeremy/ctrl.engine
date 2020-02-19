import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ctrl.engine",
    version="0.0.1",
    author="Jeremy Kanovsky",
    author_email="kanovsky.jeremy@gmail.com",
    description="A universal control engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0xJeremy/ctrl.engine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)