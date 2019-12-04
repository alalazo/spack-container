# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.util.spack_yaml as syaml


@pytest.fixture()
def minimal_configuration():
    return {
        'spack': {
            'specs': [
                'gromacs',
                'mpich',
                'fftw precision=float'
            ],
            'container': {
                'format': 'docker',
                'base': {
                    'image': 'ubuntu:18.04',
                    'spack': 'develop'
                },
                'provisioning': 'path',
            }
        }
    }


@pytest.fixture()
def configuration_file(minimal_configuration, tmpdir):
    content = syaml.dump(minimal_configuration, default_flow_style=False)
    config_file = tmpdir / 'containerize.yaml'
    config_file.write(content)
    return str(config_file)
