# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Writers for different kind of recipes and related
convenience functions.
"""
import collections
import copy

import spack.schema.env
import spack.tengine as tengine
import spack.util.spack_yaml as syaml

from ..images import build_info, package_info

#: Caches all the writers that are currently supported
_writer_factory = {}


def writer(name):
    """Decorator to register a factory for a recipe writer.

    Each factory should take a configuration dictionary and return a
    properly configured writer that, when called, prints the
    corresponding recipe.
    """
    def _decorator(factory):
        _writer_factory[name] = factory
        return factory
    return _decorator


def recipe_writers(configuration):
    """Returns a list of recipe writers for the configuration
    passed as argument.

    Args:
        configuration: how to generate the current recipe
    """
    # FIXME: At the moment return a list with a single writer. Check later
    # FIXME: if we should generalize to multiple writers or simplify this API
    name = configuration['spack']['container']['format']
    return [_writer_factory[name](configuration)]


class PathContext(tengine.Context):
    """Generic context used to instantiate templates of recipes that
    install software in a common location and make it available
    directly via PATH.
    """
    def __init__(self, config):
        self.config = config

    @tengine.context_property
    def run(self):
        """Information related to the run image."""
        image = self.config['spack']['container']['base']['image']
        Run = collections.namedtuple('Run', ['image'])
        return Run(image=image)

    @tengine.context_property
    def build(self):
        """Information related to the build image."""

        # Map the final image to the correct build image
        run_image = self.config['spack']['container']['base']['image']
        spack_version = self.config['spack']['container']['base']['spack']
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
        """The spack.yaml file that should be used in the image"""
        import jsonschema
        # Copy in the part of spack.yaml prescribed in the configuration file
        manifest = copy.deepcopy(self.config['spack'])

        # FIXME: Here we need to know that other attributes might be incompatible,
        # FIXME: and are not related to container images, for instance gitlab-ci? or cdash?
        manifest.pop('container')

        # Ensure that a few paths are where they need to be
        manifest['config'] = syaml.syaml_dict()
        manifest['config']['install_tree'] = self.paths.store
        manifest['concretization'] = 'together'
        manifest['view'] = self.paths.view
        manifest = {'spack': manifest}

        # Validate the manifest file
        jsonschema.validate(manifest, schema=spack.schema.env.schema)

        return syaml.dump(manifest, default_flow_style=False).strip()

    @tengine.context_property
    def packages(self):
        """Additional system packages that are needed at run-time."""
        package_list = self.config.get('packages', None)
        if not package_list:
            return package_list

        image = self.config['spack']['container']['base']['image']
        update, install, clean = package_info(image)
        Packages = collections.namedtuple(
            'Packages', ['update', 'install', 'list', 'clean']
        )
        return Packages(update=update, install=install,
                        list=package_list, clean=clean)

    def __call__(self):
        """Prints the recipe."""
        env = tengine.make_environment()
        t = env.get_template(self.template_name)
        print(t.render(**self.to_dict()))


# Import after function definition all the modules in this package,
# so that registration of writers will happen automatically
import spack.extensions.container.writers.singularity
import spack.extensions.container.writers.docker

