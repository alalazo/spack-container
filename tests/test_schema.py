# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# FIXME: this needs to be fixed, the command here is necessary
# FIXME: to trigger loading of extensions during tests
import spack.main
containerize = spack.main.SpackCommand('containerize')

import spack.extensions.container.images as images
import spack.extensions.container.schema as schema


def test_images_in_schema():
    allowed_images = set(
        schema.schema['properties']['base']['properties']['image']['enum']
    )
    images_in_json = set( x for x in images.data())
    assert images_in_json == allowed_images
