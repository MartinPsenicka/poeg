from os.path import dirname, join
from setuptools import setup, find_packages
import poeg


def parse_reqs(f='requirements.txt'):
    ret = []
    with open(join(dirname(__file__), f)) as fp:
        for l in fp.readlines():
            l = l.strip()
            if l and not l.startswith('#'):
                ret.append(l)
    return ret

setup_requires = ['setuptools']
install_requires, tests_require = parse_reqs(), parse_reqs('requirements-test.txt')

setup(
    name='poeg',
    version=poeg.__versionstr__,
    description='Escape',
    license='Proprietal',
    url='http://pragueoutdoorescapegames.cz',

    packages=find_packages(),
    include_package_data=True,

    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require
)
