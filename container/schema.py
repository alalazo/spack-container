# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'File schema for container recipe generation',
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'singularity': {
            'type': 'object',
            'default': {},
            'properties': {
                # The base image we want to start from
                'base_image': {
                    'type': 'string',
                    'enum': [
                        'ubuntu:18.04'
                    ]
                },
                # The spack environment used for the installation.
                # It can be either a path to a file or embedded below.
                'manifest': {
                    'anyOf': [{
                        'type': 'string'
                    }]
                }


            }
        }
    }
}
