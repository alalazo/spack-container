# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import copy

import spack.schema.env

# We need to take control of a few configuration details
# to generate
manifest_schema = copy.deepcopy(
    spack.schema.env.schema['patternProperties']['^env|spack$']
)
del manifest_schema['properties']['concretization']
del manifest_schema['properties']['view']

config_schema = manifest_schema['properties']['config']
del config_schema['properties']['install_tree']
config_schema['additionalProperties'] = False

schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'File schema for container recipe generation',
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
                    'enum': ['ubuntu:18.04']
                },
                'spack': {
                    'type': 'string',
                    'enum': ['develop', 'prerelease']
                }
            }
        },
        # Describes how we want to make the executables and
        # libraries available to users.
        'provisioning': {
            'type': 'string',
            'enum': ['path']
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
        'manifest': manifest_schema,
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
    'required': ['format', 'base', 'provisioning', 'manifest']
}
