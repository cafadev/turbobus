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
    description='TurboBus is a powerful Python package designed to streamline the development of software applications adhering to the Command Responsibility Segregation (CRS) pattern.',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Christopher A. Flores',
    author_email='cafadev@outlook.com',

    url='https://github.com/cafadev/turbobus',
    download_url=f'https://github.com/cafadev/turbobus/releases/tag/v{version}',
    keywords=['command', 'bus', 'cqrs', 'crs', 'injection', 'ddd', 'domain', 'driven', 'design', 'pattern', 'python', 'turbobus'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)