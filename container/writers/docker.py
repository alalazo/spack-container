# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.tengine as tengine

from . import writer, PathContext


class DockerContext(PathContext):
    pass


@writer('docker')
def writer_factory(configuration):
    def _impl():
        env = tengine.make_environment()
        t = env.get_template('Dockerfile')

        context = DockerContext(configuration)

        print(t.render(**context.to_dict()))
    return _impl
