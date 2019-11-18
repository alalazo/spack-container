# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


def to_sh_commands(environment_dict):
    # FIXME: This is a placeholder with the output needed to
    # FIXME: build on Ubuntu 18.04
    return """
export FORCE_UNSAFE_CONFIGURE=1
export DEBIAN_FRONTEND=noninteractive
""".strip().split('\n')
