import ast
import glob

from setuptools import setup, find_packages


with open('.project_metadata.py') as meta_file:
    project_metadata = ast.literal_eval(meta_file.read())


setup(
    name=project_metadata['name'],
    version=project_metadata['release'],
    author=project_metadata['author'],
    author_email=project_metadata['author_email'],
    description=project_metadata['description'],

    install_requires=[
        'Flask',
        'flask-marshmallow',
        'Flask-Migrate',
        'Flask-RESTPlus',
        'inflection',
        'pprintpp',
        'psycopg2',
        'py-buzz',
        'sqlparse',
        'uwsgi',
        'Flask-SQLAlchemy',
        'pydon',
        'logbook',
    ],
    extras_require={
        'dev': [
            'flake8',
            'freezegun',
            'mock',
            'pep8-naming',
            'pytest',
            'pytest-catchlog',
            'pytest-flask',
            'sphinx',
            'sphinx-view',
            'snakeviz',
        ],
    },
    include_package_data=True,
    packages=find_packages(),
    scripts=glob.glob('bin/*'),
)
