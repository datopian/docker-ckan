##################
### Build CKAN ###
##################
FROM alpine:3.18.8 AS ckanbuild

# Used by Github Actions to tag the image with
ENV IMAGE_TAG=ckan-2.10.0.alpine-3.18

# Set CKAN version to build
ENV GIT_URL=https://github.com/ckan/ckan.git
ENV GIT_BRANCH=ckan-2.10.5

# Set src dirs
ENV SRC_DIR=/srv/app/src
ENV PIP_SRC=${SRC_DIR}

WORKDIR ${SRC_DIR}

# Packages to build CKAN requirements and plugins
RUN apk add --no-cache \
        git \
        curl \
        python3 \
        postgresql-dev \
        linux-headers \
        gcc \
        make \
        g++ \
        autoconf \
        automake \
        libtool \
        patch \
        musl-dev \
        pcre-dev \
        pcre \
        python3-dev \
        libffi-dev \
        libxml2-dev \
        libxslt-dev \
        linux-headers \
        openssl-dev \
        libffi-dev \
        cargo

# Link python to python3
#RUN ln -s /usr/bin/python3 /usr/bin/python

# Create the src directory
RUN mkdir -p ${SRC_DIR}

# Install pip
RUN curl -o ${SRC_DIR}/get-pip.py https://bootstrap.pypa.io/get-pip.py && \
    python ${SRC_DIR}/get-pip.py

# Downgrade setuptools so that CKAN requirements can be built
RUN pip install setuptools==44.1.0

# Fetch and build CKAN and requirements
RUN pip install -e git+${GIT_URL}@${GIT_BRANCH}#egg=ckan
# Copy patches and apply patches script
#COPY ./patches ${SRC_DIR}/patches
#COPY ./scripts/apply_ckan_patches.sh ${SRC_DIR}/apply_ckan_patches.sh
#RUN chmod +x ${SRC_DIR}/apply_ckan_patches.sh
# Apply patches
#RUN ${SRC_DIR}/apply_ckan_patches.sh
RUN rm -rf /srv/app/src/ckan/.git
COPY requirements.txt ckan/requirements.txt
RUN pip wheel --wheel-dir=/wheels -r ckan/requirements.txt
RUN pip wheel --wheel-dir=/wheels uwsgi gevent greenlet>=2.0.0

###########################
### Default-Extensions ####
###########################
FROM alpine:3.18.8 AS extbuild

# Set src dirs
ENV SRC_DIR=/srv/app/src
ENV PIP_SRC=${SRC_DIR}

# List of default extensions
ENV DEFAULT_EXTENSIONS envvars

# Locations and tags, please use specific tags or revisions
ENV ENVVARS_GIT_URL=https://github.com/okfn/ckanext-envvars
ENV ENVVARS_GIT_BRANCH=0.0.1

RUN apk add --no-cache \
        git \
        curl \
        python3 \
        python3-dev

# Link python to python3
#RUN ln -s /usr/bin/python3 /usr/bin/python

# Create the src directory
RUN mkdir -p ${SRC_DIR}

# Install pip
RUN curl -o ${SRC_DIR}/get-pip.py https://bootstrap.pypa.io/get-pip.py && \
    python ${SRC_DIR}/get-pip.py

# Fetch and build the default CKAN extensions
RUN pip wheel --wheel-dir=/wheels git+${ENVVARS_GIT_URL}@${ENVVARS_GIT_BRANCH}#egg=ckanext-envvars

############
### MAIN ###
############
FROM alpine:3.18.8

ENV APP_DIR=/srv/app
ENV SRC_DIR=/srv/app/src
ENV CKAN_DIR=${SRC_DIR}/ckan
ENV DATA_DIR=/srv/app/data
ENV PIP_SRC=${SRC_DIR}
ENV CKAN_SITE_URL=http://localhost:5000
ENV CKAN__PLUGINS envvars image_view text_view recline_view datastore datapusher

# Install necessary packages to run CKAN
RUN apk add --no-cache git \
        bash \
        gettext \
        curl \
        postgresql-client \
        python3 \
        libmagic \
        pcre \
        libxslt \
        libxml2 \
        tzdata \
        apache2-utils && \
    # Create SRC_DIR
    mkdir -p ${SRC_DIR}
    # Link python to python3
    #ln -s /usr/bin/python3 /usr/bin/python

# Install pip
RUN curl -o ${SRC_DIR}/get-pip.py https://bootstrap.pypa.io/get-pip.py && \
    python ${SRC_DIR}/get-pip.py

# Get artifacts from build stages
COPY --from=ckanbuild /wheels /srv/app/wheels
COPY --from=extbuild /wheels /srv/app/ext_wheels
COPY --from=ckanbuild /srv/app/src/ckan ${CKAN_DIR}

# Additional install steps for build stages artifacts
RUN pip install --no-index --find-links=/srv/app/wheels uwsgi gevent greenlet>=2.0.0

# Create a local user and group to run the app
RUN addgroup -g 92 -S ckan && \
    adduser -u 92 -h /srv/app -H -D -S -G ckan ckan

WORKDIR ${CKAN_DIR}

# Install CKAN
RUN pip install -e /srv/app/src/ckan && \
    #cp who.ini ${APP_DIR} && \
    pip install --no-index --find-links=/srv/app/wheels -r requirements.txt && \
    # Install default CKAN extensions
    pip install --no-index --find-links=/srv/app/ext_wheels ckanext-envvars && \
    # Create and update CKAN config
    # Set timezone
    echo "UTC" >  /etc/timezone && \
    # Generate CKAN config
    ckan generate config ${APP_DIR}/production.ini && \
    # Configure plugins
    ckan config-tool ${APP_DIR}/production.ini "ckan.plugins = ${CKAN__PLUGINS}" && \
    # Create the data directory
    mkdir ${DATA_DIR} && \
    # Webassets can't be loaded from env variables at runtime, it needs to be in the config so that it is created
    ckan config-tool ${APP_DIR}/production.ini "ckan.webassets.path = ${DATA_DIR}/webassets" && \
    # Set the default level for extensions to INFO
    ckan config-tool ${APP_DIR}/production.ini -s logger_ckanext -e level=INFO && \
    chown -R ckan:ckan /srv/app

ENV GIT_BRANCH=dev-v2.10
ADD https://raw.githubusercontent.com/ckan/ckan/${GIT_BRANCH}/wsgi.py ${APP_DIR}
RUN pip install setuptools==44.1.0
# Remove wheels
RUN rm -rf /srv/app/wheels /srv/app/ext_wheels

# Install Dev requirements
RUN pip install -r https://raw.githubusercontent.com/ckan/ckan/ckan-2.10.0/dev-requirements.txt
# Copy necessary scripts
COPY setup/start_ckan.sh ${APP_DIR}

WORKDIR ${APP_DIR}


RUN pip3 install supervisor && \
    mkdir /etc/supervisord.d

COPY setup/supervisord.conf /etc
RUN chown -R ckan:ckan ${APP_DIR}
RUN mkdir -p /var/lib/ckan
RUN chown -R ckan:ckan /var/lib/ckan
COPY setup/supervisor.worker.conf /etc/supervisord.d/worker.conf

# Create entrypoint
ONBUILD RUN mkdir docker-entrypoint.d

# Create afterinit directory for children image scripts
ONBUILD RUN mkdir docker-afterinit.d

EXPOSE 5000

USER ckan

CMD ["/srv/app/start_ckan.sh"]
