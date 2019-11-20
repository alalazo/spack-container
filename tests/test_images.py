# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

# FIXME: this needs to be fixed, the command here is necessary
# FIXME: to trigger loading of extensions during tests
import spack.main
containerize = spack.main.SpackCommand('containerize')

import spack.extensions.container.images as images


@pytest.mark.parametrize('image,spack_version,expected', [
    ('ubuntu:18.04', 'develop', ('spack/ubuntu-bionic', 'latest')),
    ('ubuntu:18.04', 'prerelease', ('spack/ubuntu-bionic', 'prerelease')),
])
def test_build_info(image, spack_version, expected):
    output = images.build_info(image, spack_version)
    assert output == expected


@pytest.mark.parametrize('image,spack_version', [
    ('ubuntu:18.04', 'doesnotexist')
])
def test_build_info_error(image, spack_version):
    with pytest.raises(ValueError, match=r"has no tag for"):
        images.build_info(image, spack_version)


@pytest.mark.parametrize('image', [
    'ubuntu:18.04'
])
def test_package_info(image):
    update, install, clean = images.package_info(image)
    assert update
    assert install
    assert clean
