from setuptools import setup

readme = open("./README.md", "r")


setup(
    name='turbobus',
    packages=['turbobus'],
    version='1.0.0-alpha.1',
    description='TurboBus is an opinionated implementation of Command Responsibility Segregation pattern in python.',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Christopher A. Flores',
    author_email='cafadev@outlook.com',

    url='https://github.com/cafadev/turbobus',
    download_url='https://github.com/cafadev/turbobus/releases/tag/v1.0.0-alpha.1',
    keywords=['command', 'bus', 'cqrs', 'commandbus', 'ddd'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)