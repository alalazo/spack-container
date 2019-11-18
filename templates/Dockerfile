# The first stage is an Ubuntu bionic image
# with Spack pre-installed and ready to be used
FROM {{ build.image }}:{{ build.tag }} as builder

# What we want to install and how we want to install it
# is specified in a manifest file (spack.yaml)
RUN mkdir {{ paths.environment }} \
{{ manifest }} > {{ paths.environment }}/spack.yaml

# Spack can do constraint resolution and install all the software
# in a single command.
RUN cd {{ paths.environment }} && spack install && spack autoremove -y
RUN cd {{ paths.view }}/bin && strip -s * || exit 0
RUN cd {{ paths.view }}/lib && strip -s * || exit 0

# Spack is aware of modifications to the environment that are
# necessary to run an application.
RUN cd {{ paths.environment }} && \
    spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh

# The second stage is a bare Ubuntu bionic image where we copy
# the artifacts generated during the first stage
FROM {{ run.image }}

COPY --from=builder {{ paths.environment }} {{ paths.environment }}
COPY --from=builder {{ paths.store }} {{ paths.store }}
COPY --from=builder {{ paths.view }} {{ paths.view }}
COPY --from=builder /etc/profile.d/z10_spack_environment.sh /etc/profile.d/z10_spack_environment.sh

{% if packages %}
RUN {{ packages.update }}                                   \
 && {{ packages.install }}{% for pkg in packages.list %} {{ pkg }}{% endfor %} \
 && {{ packages.clean }}
{% endif %}

ENTRYPOINT ["/bin/bash", "--rcfile", "/etc/profile", "-l"]
