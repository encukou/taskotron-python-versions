import glob
import os

import pytest

from taskotron_python_versions.common import Package
from taskotron_python_versions.two_three import check_two_three


def pkg(filename):
    return os.path.join(os.path.dirname(__file__), '..', 'fixtures', filename)


def gpkg(pkgglob):
    return Package(glob.glob(pkg(pkgglob))[0])


@pytest.mark.parametrize('pkgglob', ('pyserial*', 'python-peak-rules*',
                                     'python2-geoip2*'))
def test_package_depends_on_2_only(pkgglob):
    name, versions = check_two_three(gpkg(pkgglob))
    assert 2 in versions
    assert 3 not in versions


@pytest.mark.parametrize('pkgglob', ('python3-pyserial*',))
def test_package_depends_on_3_only(pkgglob):
    name, versions = check_two_three(gpkg(pkgglob))
    assert 2 not in versions
    assert 3 in versions


@pytest.mark.parametrize('pkgglob', ('tracer*',))
def test_package_depends_on_2_and_3(pkgglob):
    name, versions = check_two_three(gpkg(pkgglob))
    assert 2 in versions
    assert 3 in versions


@pytest.mark.parametrize('pkgglob', ('libgccjit-devel*',))
def test_package_depends_on_no_python(pkgglob):
    name, versions = check_two_three(gpkg(pkgglob))
    assert not versions
