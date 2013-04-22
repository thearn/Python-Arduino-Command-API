from setuptools import setup, find_packages

setup(name='Python Arduino Command API',
    version='',
    description="a light-weight Python library for communicating with Arduino microcontroller boards",
    long_description='',
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    install_requires=['pyserial >= 2.6'],
    keywords='',
    author='Tristan Hearn',
    author_email='tristanhearn@gmail.com',
    url='https://github.com/thearn/Python-Arduino-Command-API',
    license='Apache 2.0',
    packages=find_packages('Arduino'),
    package_dir = {'': 'Arduino'},
    include_package_data=True,
    zip_safe=False
)
