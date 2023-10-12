import json
from setuptools import setup
readme = open("./README.md", "r")


json_data = {}

with open('./turbobus/version_output.json') as f:
    json_data = json.load(f)

    
version = json_data.get('version')

print(version)

if version is None:
    raise Exception('Unprocessable without version')

setup(
    name='turbobus',
    packages=['turbobus'],
    version=version,
    description='TurboBus is an opinionated implementation of Command Responsibility Segregation pattern in python.',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Christopher A. Flores',
    author_email='cafadev@outlook.com',

    url='https://github.com/cafadev/turbobus',
    download_url=f'https://github.com/cafadev/turbobus/releases/tag/v{version}',
    keywords=['command', 'bus', 'cqrs', 'commandbus', 'ddd'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)