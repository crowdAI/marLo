from setuptools import setup, find_packages

setup(name='marlo',
      version='0.0.1dev2',
      description='Marlo',
      url='https://github.com/spMohanty/marlo',
      author='S.P. Mohanty',
      author_email='sharada.mohanty@epfl.ch',
      license='MIT License',
      packages=find_packages(),
      package_data={'': ['assets/*.xml']},
      zip_safe=False,
      install_requires=['malmo', 'gym', 'lxml', 'psutil', 'chainerrl', 'pillow'],
      dependency_links=[]
)
