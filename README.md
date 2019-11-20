Manage the build of your container images using Spack!

## Quickstart

To use the extension clone this repository in a folder of your choice:
```console
$ cd /home/user/.spack/extensions
$ git clone https://github.com/alalazo/spack-container.git
``` 
Then add that folder to Spack's `config.yaml`:
```yaml
config:
  extensions:
  - /home/user/.spack/extensions/spack-container
```
At this point you're ready to go! You should be able 
to find the new command that the extension provides and check
its help:
```console
$ spack containerize -h
usage: spack containerize [-h] [--config CONFIG]

creates recipes to build images for different container runtimes

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  configuration for the container recipe that will be generated
```

## Configuration file
The command currently provided takes as input a YAML
configuration file. Its format is currently experimental
and might change drastically. As an example you can check 
out the following:
```yaml
# Select the format of the recipe e.g. docker,
# singularity or anything else that is currently supported
format: docker

# Select from a valid list of images
base:
  image: "ubuntu:18.04"
  spack: prerelease

# Provisioning is how we want to make the executables available
# to the user. At the moment the only value possible is:
#
# 1. path (implies "concretization: together", views in "opt/view")
provisioning: path

# Additional system packages that are needed at runtime
packages:
- libgomp1

# Manifest that describes installation and configuration.
# This is basically a spack.yaml entry with a few field that 
# can't be set 
manifest:
  specs:
  - gromacs build_type=Release 
  - mpich
  - fftw precision=float
  packages:
    all:
      target: [broadwell]

# Any label that we want to add to the container
labels:
  target: "broadwell"
```
