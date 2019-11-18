# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.schema.env

properties = {

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
    'manifest': {
        # TODO: The spack environment used for the installation.
        # TODO: It can be either a path to a file or embedded below.
        'manifest': {
            'anyOf': [{
                'type': 'string'
            }, spack.schema.env.schema]
        },
        # TODO: Limit the schema above with the sections that
        # TODO: are not allowed
    },
    'environment': {
        'type': 'array'
        # TODO: implement this later
    },
    'labels': {
        'type': 'object',
    }
    # TODO: add properties for options that are specific to each format
    # 'singularity': {
    #    'type': 'object',
    #    'default': {},
    # }
}

schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'File schema for container recipe generation',
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'containerize': {
            'type': 'object',
            'type': 'object',
            'additionalProperties': False,
            'properties': properties,
            'required': ['format', 'base', 'provisioning']
        }
    }
}
