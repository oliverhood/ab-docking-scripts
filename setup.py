from setuptools import setup, find_packages

setup(
    name='abagdocking',
    version='1.0.0',
    author='ChuNan Liu',
    author_email='chunan.liu@ucl.ac.uk',
    description='A wrap up around commonly used docking methods',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
            'split_abag_chains = abagdocking.common.split_abag_chains:app',
            'get_fasta = abagdocking.common.get_fasta:app',
        ],
    },
)