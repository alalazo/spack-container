# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import copy

import spack.schema.env

# We need to take control of a few configuration details
# to generate an image correctly
manifest_schema = copy.deepcopy(
    spack.schema.env.schema['patternProperties']['^env|spack$']
)
del manifest_schema['properties']['concretization']
del manifest_schema['properties']['view']

config_schema = manifest_schema['properties']['config']
del config_schema['properties']['install_tree']
config_schema['additionalProperties'] = False

# Options that are specific to container image generation
container = {}

container_schema = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        # The recipe formats that are currently supported by the command
        'format': {
            'type': 'string',
            'enum': ['docker', 'singularity']
        },
        # Describes the base image to start from and the version
        # of Spack to be used
        'base': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'image': {
                    'type': 'string',
                    'enum': ['ubuntu:18.04', 'ubuntu:16.04', 'centos:7', 'centos:6']
                },
                'spack': {
                    'type': 'string',
                    'enum': ['develop', 'prerelease', '0.13.2']
                }
            }
        },
        # Additional system packages that are needed at runtime
        'packages': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        },
        # The portion of Spack environment file that can be used
        # to describe what to install and how to configure it
        'environment': {
            'type': 'array'
            # TODO: implement this later, it needs #spack/13357
        },
        'labels': {
            'type': 'object',
        }
        # TODO: add properties for options that are specific to each format
        # 'singularity': {
        #    'type': 'object',
        #    'default': {},
        # }
        # 'docker': {
        #    'type': 'object',
        #    'default': {},
        # }
    },
    'required': ['format', 'base']
}

manifest_schema['properties']['container'] = container_schema

schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack environment file schema',
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': {
        '^env|spack$': manifest_schema
    }
}
