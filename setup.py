"""Packaging wheel."""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="denz-seah-fake-data-builder",
    version="0.0.1",
    author="Dennis Seah",
    author_email="dennis.seah@gmail.com",
    description="Generating data with Faker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dennisseah/fakedatagen",
    project_urls={
        "Bug Tracker": "https://github.com/dennisseah/fakedatagen/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=["pandas>=1.3.3", "faker>=8.14.0"],
)
