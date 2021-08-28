from setuptools import find_packages, setup
setup(
    name='FASTGate',
    packages=find_packages(),
    version='0.1.0',
    description='Api for remote command of router FASTGate given by Fastweb',
    author='drGremi',
    license='GPLv2',
    install_requires=['requests']
)
