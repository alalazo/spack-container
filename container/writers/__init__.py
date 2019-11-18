# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
_known_writers = {}


def writer(name):
    """Decorator to register a factory for a recipe writer."""
    def _decorator(func):
        _known_writers[name] = func
        return func
    return _decorator


def recipe_writers(configuration):
    """Returns a list of recipe writers for the configuration
    passed as argument.

    Args:
        configuration: how to generate the current recipe
    """
    # FIXME: At the moment return a list with a single writer. Check later
    # FIXME: if we should generalize multiple writers or simplify this API
    name = configuration['format']
    return [_known_writers[name](configuration)]

# Import after function definition all the modules in this package,
# so that registration of writers will happen automatically
import spack.extensions.container.writers.singularity
import spack.extensions.container.writers.docker

