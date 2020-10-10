from setuptools import setup

setup(
      name = 'robotframework-hangsafelibrary',
      version = '0.2.0',
      description = 'For impelementing timeout keyword in case of python hanging (particularly in Windows)',
      author = 'Simo Soininen',
      author_email = 'soinisi@gmail.com',
      license = 'MIT',
      packages = ['HangsafeLibrary'],
      install_requires = ['robotframework'],
      setup_requires = ['pytest-runner'],
      tests_require=['pytest'],
      platforms=['Linux', 'Unix', 'Windows', 'MacOS X'],
      )