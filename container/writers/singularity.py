# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.tengine as tengine

from . import writer, PathContext


class SingularityContext(PathContext):
    pass


@writer('singularity')
def writer_factory(container_config):
    def _impl():
        env = tengine.make_environment()
        t = env.get_template('singularity.def')

        context = SingularityContext(container_config)

        print(t.render(**context.to_dict()))
    return _impl
