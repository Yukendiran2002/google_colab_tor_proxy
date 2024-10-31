from setuptools import setup, find_packages

setup(
    name="tor_privoxy_setup",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  # Add any dependencies if needed
    author="Yukendiran",
    author_email="yukendiranjayachandiran@gmail.com",
    description="A tool for installing and configuring Tor and Privoxy.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Yukendiran2002/google_colab_tor_proxy_setup",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
    ],
    python_requires=">=3.6",
)
