from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

with open("requirements.txt", "r") as f:
        install_requires = [x.strip() for x in f.readlines() if not x.startswith("#")]


setup(name='sra',
      version='0.99.0',
      description='download and convert sra files',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
      ],
      keywords='sra, fastq',
      url='http://github.com/lpantano/sra',
      author='Lorena Pantano',
      author_email='lpantano@iscb.org',
      license='MIT',
      packages=find_packages(),
      install_requires=install_requires,
      test_suite='nose',
      include_package_data=True,
      zip_safe=False)
