import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# To allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangocms-tacc-page-export',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A Django CMS app (for TACC Core CMS) to export rendered page content to DOCX.',
    long_description=README,
    url='https://github.com/TACC/Core-CMS-Plugin-Page-Export/',
    author='TACC ACI WMA, TACC COA CMD',
    author_email='wma-portals@tacc.utexas.edu, coa-cmd@tacc.utexas.edu',
    # SEE: https://packaging.python.org/discussions/install-requires-vs-requirements/
    install_requires=[
        'Django>=3.2',
        'django-cms>=3.7.4,<4',
        'python-docx>=1.1.0',
    ],
    # SEE: https://pypi.org/classifiers/
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
