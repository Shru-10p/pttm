from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="ts-pmo",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "pmo": ["pmo.css"],
    },
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "pttm=pmo.app:main",
        ],
    },
)
