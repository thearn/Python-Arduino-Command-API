from setuptools import setup

setup(name='Python Arduino Command API',
    version='0.1',
    install_requires=['pyserial >= 2.6'],
    description="a light-weight Python library for communicating with Arduino microcontroller boards",
    author='Tristan Hearn',
    author_email='tristanhearn@gmail.com',
    url='https://github.com/thearn/pickle-gzip',
    license='Apache 2.0',
    packages=['Arduino'],
)
