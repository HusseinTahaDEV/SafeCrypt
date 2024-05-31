from setuptools import setup, find_packages

setup(
    name="safecrypt",
    version="0.1.0",
    description="file encryption and decryption tool",
    author="Hussein taha",
    author_email="ceo.husseintaha@gamil.com",
    url="https://github.com/HusseinTahaDEV/SafeCrypt",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "PyQt5",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "safecrypt=safecrypt.main:main",
        ],
    },
)
