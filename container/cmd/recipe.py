# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.environment
import spack.util.spack_yaml as syaml

from ..schema import schema
from ..writers import recipe_writers

description = ("creates recipes to build images for different"
               " container runtimes")
section = "container"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '--config', default='./containers.yaml',
        help='configuration for the container recipes that are to be generated'
    )
    subparser.add_argument(
        '--environment', default='./spack.yaml',
        help='Spack environment with the list of specs to build'
    )


def recipe(parser, args):
    # Validate containers against the schema
    import jsonschema
    with open(args.config) as f:
        container_config = syaml.load(f)
    jsonschema.validate(container_config, schema=schema)

    # Validate the environment
    with open(args.environment) as f:
        environment_config = syaml.load(f)
    spack.environment.validate(environment_config)

    # Write recipes according to configuration
    for writer in recipe_writers(environment_config, container_config):
        # TODO: make it a class to have more opportunities of extension?
        writer()
