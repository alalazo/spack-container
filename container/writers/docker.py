# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections

import spack.tengine as tengine
import spack.util.spack_yaml as syaml

from . import writer
from ..system import build_info, package_info


class DockerContext(tengine.Context):
    def __init__(self, config):
        # FIXME: this is already unwrapped
        self.config = config

    @tengine.context_property
    def run(self):
        """Information related to the run image."""
        image = self.config['base']['image']
        Run = collections.namedtuple('Run', ['image'])
        return Run(image=image)

    @tengine.context_property
    def build(self):
        """Information related to the build image."""

        # Map the final image to the correct build image
        run_image = self.config['base']['image']
        spack_version = self.config['base']['spack']
        image, tag = build_info(run_image, spack_version)

        Build = collections.namedtuple('Build', ['image', 'tag'])
        return Build(image=image, tag=tag)

    @tengine.context_property
    def paths(self):
        """Important paths in the image"""
        Paths = collections.namedtuple('Paths', [
            'environment', 'store', 'view'
        ])
        return Paths(
            environment='/opt/spack-environment',
            store='/opt/software',
            view='/opt/view'
        )

    @tengine.context_property
    def manifest(self):
        # Copy in the part of spack.yaml prescribed in the configuration file
        manifest = self.config['manifest']

        # Ensure that a few paths are where they need to be
        manifest['config'] = syaml.syaml_dict()
        manifest['config']['install_tree'] = self.paths.store
        manifest['concretization'] = 'together'
        manifest['view'] = self.paths.view
        manifest = {'spack': manifest}

        # Decorate things
        manifest_str = syaml.dump(manifest, default_flow_style=False).strip()
        echoed_lines = []
        for idx, line in enumerate(manifest_str.split('\n')):
            if idx == 0:
                echoed_lines.append('&&  (echo "' + line + '" \\')
                continue
            echoed_lines.append('&&   echo "' + line + '" \\')

        echoed_lines[-1] = echoed_lines[-1].replace(' \\', ')')

        return '\n'.join(echoed_lines)

    @tengine.context_property
    def packages(self):
        package_list = self.config.get('packages', None)
        if not package_list:
            return package_list

        image = self.config['base']['image']
        update, install, clean = package_info(image)
        Packages = collections.namedtuple(
            'Packages', ['update', 'install', 'list', 'clean']
        )
        return Packages(update=update, install=install,
                        list=package_list, clean=clean)


@writer('docker')
def writer_factory(configuration):
    def _impl():
        env = tengine.make_environment()
        t = env.get_template('Dockerfile')

        context = DockerContext(configuration)

        print(t.render(**context.to_dict()))
    return _impl
