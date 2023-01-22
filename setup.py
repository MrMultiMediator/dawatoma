from setuptools import setup, find_packages

setup(name='dawatoma',
      version='0.2.1b5',
      packages=find_packages(),
      description='DAW Automation: music idea generation software',
      package_dir={'':'.'},
      install_requires=[
        "MIDIUtil>=1.2.1",
        "attrs>=21.2.0"
        ],
      author='MrMultiMediator',
      author_email='mrmultimediator@gmail.com',
      url='https://www.mrmultimediator.github.io/',
     )

"""
setup(name='dawatoma',
      version='0.2.1b3',
      description='DAW Automation: music idea generation software',
      package_dir={'':'dawatoma'},
      packages=find_packages('dawatoma'),
      install_requires=[
        "MIDIUtil>=1.2.1",
        "attrs>=21.2.0"
        ],
      author='MrMultiMediator',
      author_email='mrmultimediator@gmail.com',
      url='https://www.mrmultimediator.github.io/',
     )
"""
