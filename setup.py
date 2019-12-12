from setuptools import setup, find_packages

setup(
    name='helper',
    version='0.0.1',
    description='Helper scripts for everyday life',
    url='',
    author=['Laurits Tani'],
    author_email='',
    license='MIT',
    packages=find_packages(),
    package_data={
        'helper': [
            'tests/*', ]
    },
    install_requires=[
        'docopt',
        'numpy',
        'bcolors'
    ],
)