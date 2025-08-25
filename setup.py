from setuptools import setup

AUTHOR_NAME='ROHIT SINGH'
SRC_REPO='src'
LIST_OF_REQUIREMENTS=['streamlit']

setup(
    name=SRC_REPO,
    version='0.0.1',
    author=AUTHOR_NAME,
    author_email='rohitpramodsingh@gmail.com',
    long_description_content_type='text/markdown',
    package=[SRC_REPO],
    Python_Requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS,
)