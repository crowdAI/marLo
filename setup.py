from setuptools import setup, find_packages

setup(name='marlo',
      version='0.0.1dev18',
      description='Marlo',
      url='https://github.com/crowdAI/marlo',
      author='S.P. Mohanty',
      author_email='sharada.mohanty@epfl.ch',
      license='MIT License',
      packages=find_packages(),
      package_data = {
        '':['envs/*/templates/*.xml']
      },
      zip_safe=False,
      install_requires=['gym', 'jinja2', 'lxml', 'crowdai_api>=0.1.18'],
      dependency_links=[]
)
