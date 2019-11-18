# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

import spack.environment
import spack.tengine as tengine
import spack.util.spack_yaml as syaml

from . import writer
from ..system import get
from ..environment import to_sh_commands


class SingularityContext(tengine.Context):
    def __init__(self, singularity_config):
        """Context used to generate templates for singularity.

        Args:
            singularity_config (dict): configurations specific to the
                Singularity definition file to be generated
        """
        self.singularity_config = singularity_config

        manifest = singularity_config['manifest']

        # If manifest is not a mapping, it's a path to the
        # corresponding spack.yaml file that needs to be read
        if not isinstance(manifest, Mapping):
            with open(manifest) as f:
                manifest = syaml.load(f)

        # FIXME: The copy is needed not to pollute the spack.yaml file
        # FIXME: with default values for attributes
        import copy
        m = copy.deepcopy(manifest)
        spack.environment.validate(m)

        if singularity_config['provisioning'] == 'path':
            s = manifest['spack']
            # TODO: Add warnings if there's conflicting configuration
            s['concretization'] = 'together'
            s['view'] = '/opt/view'
            s.setdefault('config', {})['install_tree'] = '/opt/software'
        else:
            raise RuntimeError('only "path" provisioning supported for the time being supported')

        self.environment_config = manifest

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

        base_os, _, version = self.base_image.partition(':')

        # Construct the dictionary with the information needed to setup the
        # base image with a working Spack installation
        info = get('singularity', base_os)
        version_info = info.pop('versions')
        if version in version_info:
            info.update(version_info[version])

        # FIXME: this needs to be generalized, the current implementation
        # FIXME: is a placeholder.
        if 'environment' in info:
            info['environment'] = to_sh_commands(info['environment'])

        # TODO: assert that everything expected is in the dict

        return System(info)

    @tengine.context_property
    def environment(self):
        return syaml.dump(self.environment_config, default_flow_style=False)

    @tengine.context_property
    def apps(self):
        return self.singularity_config.get('apps', {})

    @tengine.context_property
    def labels(self):
        """Labels that will be added to the container image."""
        return self.singularity_config.get('labels', {})


@writer('singularity')
def writer_factory(container_config):
    def _impl():
        env = tengine.make_environment()
        t = env.get_template('singularity.def')

        context = SingularityContext(container_config)

        print(t.render(**context.to_dict()))
    return _impl
