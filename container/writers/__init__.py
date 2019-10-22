# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
_known_writers = {}


def writer(name):
    def _decorator(func):
        _known_writers[name] = func
        return func
    return _decorator


def recipe_writers(environment_config, container_config):
    writers = []
    for container_name, writer_factory in _known_writers.items():
        # If we don't have a corresponding section move on
        if container_name not in container_config:
            continue

        writers.append(writer_factory(environment_config, container_config[container_name]))
    return writers

# Import after function definition all the modules in this package,
# so that registration of writers will happen automatically
import spack.extensions.container.writers.singularity
