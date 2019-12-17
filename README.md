![](https://github.com/alalazo/spack-container/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/alalazo/spack-container/branch/master/graph/badge.svg)](https://codecov.io/gh/alalazo/spack-container)

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
If you want to generate a recipe in e.g. a `Dockerfile`
format all you need to do is point the command to the YAML 
file that contains all the information needed:
```console
$ spack containerize --config=$HOME/docker/gromacs/containerize.yaml
```
The output of the command should look like:
```Dockerfile
# Build stage with Spack pre-installed and ready to be used
FROM spack/ubuntu-bionic:prerelease as builder

# What we want to install and how we want to install it
# is specified in a manifest file (spack.yaml)
RUN mkdir /opt/spack-environment \
&&  (echo "spack:" \
&&   echo "  specs:" \
&&   echo "  - gromacs build_type=Release" \
&&   echo "  - mpich" \
&&   echo "  - fftw precision=float" \
&&   echo "  packages:" \
&&   echo "    all:" \
&&   echo "      target:" \
&&   echo "      - broadwell" \
&&   echo "  config:" \
&&   echo "    install_tree: /opt/software" \
&&   echo "  concretization: together" \
&&   echo "  view: /opt/view") > /opt/spack-environment/spack.yaml

# Install the software, remove unecessary deps and strip executables
RUN cd /opt/spack-environment && spack install && spack autoremove -y
RUN cd /opt/view/bin && strip -s * || exit 0
RUN cd /opt/view/lib && strip -s * || exit 0

# Modifications to the environment that are necessary to run
RUN cd /opt/spack-environment && \
    spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh

# Bare OS image to run the installed executables
FROM ubuntu:18.04

COPY --from=builder /opt/spack-environment /opt/spack-environment
COPY --from=builder /opt/software /opt/software
COPY --from=builder /opt/view /opt/view
COPY --from=builder /etc/profile.d/z10_spack_environment.sh /etc/profile.d/z10_spack_environment.sh

RUN apt-get -yqq update && apt-get -yqq upgrade                                   \
 && apt-get -yqq install libgomp1 \
 && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/bin/bash", "--rcfile", "/etc/profile", "-l"]
```  

## Configuration file
The command currently provided takes as input a YAML
configuration file. Its format is currently experimental
and might change drastically. As an example you can check 
out the following:
```yaml
spack:
  specs:
  - gromacs build_type=Release 
  - mpich
  - fftw precision=float
  packages:
    all:
      target: [broadwell]

  container:
    # Select the format of the recipe e.g. docker,
    # singularity or anything else that is currently supported
    format: docker
    
    # Select from a valid list of images
    base:
      image: "ubuntu:18.04"
      spack: prerelease

    # Additional system packages that are needed at runtime
    packages:
    - libgomp1

    # Custom environment modifications for the runtime. These are on 
    # top of those prescribed by package recipes.
    environment:
    - action: append_path
      var: PATH
      value: /opt/view/bin
    - action: append_path
      var: LD_LIBRARY_PATH
      value: /opt/view/lib
    - action: unset
      var: LIBRARY_PATH
    
    labels:
      author: "Massimiliano Culpo"
      target: "broadwell"
```
