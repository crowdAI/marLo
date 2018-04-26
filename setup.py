from setuptools import setup, find_packages

setup(name='marlo',
      version='0.0.1',
      description='Environments for Multi Agent Reinforcement Learning \
      using MalmÖ',
      long_description=""" A collection of OpenAI Gym-like environments \
      for Multi Agent reinforcement learning tasks on MineCraft using \
      Project MalmÖ
      """,
      url='https://github.com/spMohanty/marLo',
      author='S.P. Mohanty',
      author_email='spmohanty91@gmail.com',
      license='MIT License',
      packages=find_packages(),
      package_data={'': ['marlo_env_specs/*.xml']},
      zip_safe=False,
      install_requires=['gym>=0.10.5']
)
