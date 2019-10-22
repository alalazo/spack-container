# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.tengine as tengine
from ..system import get

from . import writer


class SingularityContext(tengine.Context):
    def __init__(self, environment_config, singularity_config):
        """Context used to generate templates for singularity.

        Args:
            environment_config (dict): configurations of the packages to
                be installed i.e. spack.yaml
            singularity_config (dict): configurations specific to the
                Singularity definition file to be generated
        """
        self.environment_config = environment_config
        self.singularity_config = singularity_config

    @tengine.context_property
    def base_image(self):
        """Base image to be used in the definition file."""
        # TODO: Check this is a known base image or return a warning
        return self.singularity_config['base_image']

    @tengine.context_property
    def system(self):
        """Returns a dict with the actions needed to prepare the system
        for Spack installation.
        """
        class System(object):
            def __init__(self, info):
                self.info = info

            def __getattr__(self, item):
                if item in self.info:
                    return self.info[item]
                raise AttributeError('trying to access non-existing attribute [0]'.format(item))

        info = {}
        base_os, _, version = self.base_image.partition(':')

        info = get('singularity', base_os)
        version_info = info.pop('versions')
        if version in version_info:
            info.update(version_info[version])

        # TODO: assert that everything expected is in the dict

        return System(info)

    @tengine.context_property
    def environment(self):
        import spack.util.spack_yaml as syaml
        return syaml.dump(self.environment_config, default_flow_style=False)

    @tengine.context_property
    def labels(self):
        # TODO: implement this
        return {}


@writer('singularity')
def writer_factory(environment_config, container_config):
    def _impl():
        env = tengine.make_environment()
        t = env.get_template('singularity.def')

        context = SingularityContext(environment_config, container_config)

        print(t.render(**context.to_dict()))
    return _impl
