from setuptools import setup, find_packages

setup(
    name='food-mood-log',
    version=open('fml/VERSION').readline().strip(),
    python_requires='!=2, ~=3.9',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'fml = fml.__main__:main',
        ],
    },
    author='jsen',
    author_email='achillea@protonmail.com',
    description='Food-mood logging tool',
    keywords='',
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
    ],
    license='LGPLv3',
    url=''
)