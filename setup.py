from setuptools import setup, find_packages

setup(
    name='DiscBot',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    url='',
    license='',
    author='Mark Darroch',
    author_email='2146229D@student.gla.ac.uk',
    description='A chatbot and musicbot for Discord',
    install_requires=[
        "tensorflow==2.3.0",
        "keras==2.4.3",
        "tensorflow-datasets==1.2.0",
        "matplotlib==3.2.2",
        "discord.py[voice]==1.4.1",
        "lyricsgenius==1.8.6",
        "youtube-dl==2020.9.14",
        "pytest==5.4.3",
        "pytest-asyncio==0.14.0"
        "distest==0.4.8",
        "scipy==1.4.1",
        "aiohttp==3.6.2",
        "ftfy==5.8"
    ],
    python_requires='==3.7.4',
)
