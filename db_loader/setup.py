from setuptools import setup, find_packages

setup(
    name='db_loader',
    version='1.0',
    description='Take Deal Registration CSV tables, parse them, and add them to a database.',
    author='Kate Harbison',
    license='UNLICENSED',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'db-loader=db_loader.process_deal_reg_data:main'
        ]
    },
    install_requires=[
        'sqlalchemy',
        'sqlalchemy_utils'
    ],
    extras_require={
        'test': ['pytest']
    },
    zip_safe=False
)