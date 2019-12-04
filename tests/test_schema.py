# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.extensions.container import images
from spack.extensions.container import schema


def test_images_in_schema():
    allowed_images = set(
        schema.container_schema['properties']['base']['properties']['image']['enum']
    )
    images_in_json = set(x for x in images.data())
    assert images_in_json == allowed_images
