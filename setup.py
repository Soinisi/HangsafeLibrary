from setuptools import setup

setup(
      name = 'robotframework-HangsafeLibrary',
      version = '0.1.0',
      description = 'For impelementing timeout keyword in case of python hanging (particularly in Windows)',
      author = 'Simo Soininen',
      author_email = 'soinisi@gmail.com',
      license = 'MIT',
      packages = ['HangsafeLibrary'],
      install_requires = ['robotframework'],
      platforms=['Linux', 'Unix', 'Windows', 'MacOS X'],
      )