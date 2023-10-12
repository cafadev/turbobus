import sys
from setuptools import setup
readme = open("./README.md", "r")

from matic_release.axioma.version import Version
from matic_release.capabilities.commit_analyzer import CommitAnalyzer
from matic_release.capabilities.compute_tag import ComputeTag
from matic_release.capabilities.publish_tag import PublishTag
from matic_release.integration.git import GitService

git = GitService()

latest_tag = git.get_latest_tag()

version = Version(latest_tag)

commit_analyzer = CommitAnalyzer()
compute_tag = ComputeTag(git, commit_analyzer)

compute_tag.execute(version)


setup(
    name='turbobus',
    packages=['turbobus'],
    version=version.future_tag.value,
    description='TurboBus is an opinionated implementation of Command Responsibility Segregation pattern in python.',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Christopher A. Flores',
    author_email='cafadev@outlook.com',

    url='https://github.com/cafadev/turbobus',
    download_url=f'https://github.com/cafadev/turbobus/releases/tag/v{version.future_tag.value}',
    keywords=['command', 'bus', 'cqrs', 'commandbus', 'ddd'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)