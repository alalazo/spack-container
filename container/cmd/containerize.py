# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.util.spack_yaml as syaml

from ..schema import schema
from ..writers import recipe_writers

description = ("creates recipes to build images for different"
               " container runtimes")
section = "container"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '--config', default='./containerize.yaml',
        help='configuration for the container recipe that will be generated'
    )


def containerize(parser, args):
    # Validate containers against the schema
    import jsonschema
    with open(args.config) as f:
        config = syaml.load(f)
    jsonschema.validate(config, schema=schema)

    # Write recipes according to configuration
    for writer in recipe_writers(config):
        # TODO: make it a class to have more opportunities of extension?
        writer()
