# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import json
import os.path

_data = None


def data():
    global _data
    if not _data:
        json_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')
        json_dir = os.path.abspath(json_dir)
        json_file = os.path.join(json_dir, 'base_images.json')
        with open(json_file) as f:
            _data = json.load(f)
    return _data


def build_info(image, spack_version):
    # FIXME: Error handling is totally missing
    image_data = data()[image]
    build_image = image_data['build']
    build_tag = image_data['build_tags'][spack_version]
    return build_image, build_tag


def package_info(image):
    image_data = data()[image]
    update = image_data['update']
    install = image_data['install']
    clean = image_data['clean']
    return update, install, clean

# FIXME: Delete the function below
def get(container, operating_system):
    return data()[container][operating_system]
