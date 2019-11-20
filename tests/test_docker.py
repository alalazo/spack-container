# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.extensions.container import writers


def test_manifest(minimal_configuration):
    writer = writers.recipe_writers(minimal_configuration).pop()
    manifest_str = writer.manifest
    for line in manifest_str.split('\n'):
        assert 'echo' in line


def test_build_and_run_images(minimal_configuration):
    writer = writers.recipe_writers(minimal_configuration).pop()

    # Test the output of run property
    run = writer.run
    assert run.image == 'ubuntu:18.04'

    # Test the output of the build property
    build = writer.build
    assert build.image == 'spack/ubuntu-bionic'
    assert build.tag == 'latest'


def test_packages(minimal_configuration):
    # In this minimal configuration we don't have packages
    writer = writers.recipe_writers(minimal_configuration).pop()
    assert writer.packages is None

    # If we add them a list should be returned
    pkgs = ['libgomp1']
    minimal_configuration['packages'] = pkgs
    writer = writers.recipe_writers(minimal_configuration).pop()
    p = writer.packages
    assert p.update
    assert p.install
    assert p.clean
    assert p.list == pkgs


def test_ensure_render_works(minimal_configuration):
    # Here we just want to ensure that nothing is raised
    writer = writers.recipe_writers(minimal_configuration).pop()
    writer()
