# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.main
containerize = spack.main.SpackCommand('containerize')


def test_command(configuration_file, capsys):
    with capsys.disabled():
        output = containerize('--config={0}'.format(configuration_file))
    assert 'FROM spack/ubuntu-bionic' in output
