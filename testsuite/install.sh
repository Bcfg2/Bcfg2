#!/bin/bash -ex

# install script for Travis-CI

sudo apt-get update -qq
sudo apt-get install swig libxml2-utils

pip install -r testsuite/requirements.txt

PYVER=$(python -c 'import sys;print(".".join(str(v) for v in sys.version_info[0:2]))')

if [[ ${PYVER:0:1} == "2" && $PYVER != "2.7" ]]; then
    pip install unittest2
fi

if [[ "$WITH_OPTIONAL_DEPS" == "yes" ]]; then
    sudo apt-get install -y yum libaugeas0 augeas-lenses libacl1-dev libssl-dev \
        python-gamin python-selinux

    pip install PyYAML pyinotify boto pylibacl Jinja2 guppy cherrypy python-augeas

    if [[ ${PYVER:0:1} == "2" ]]; then
        pip install cheetah m2crypto

        if [[ $PYVER != "2.7" ]]; then
            pip install 'django<1.7' 'South<0.8' 'mercurial<4.3'
        else
            pip install django mercurial
        fi
    fi
fi
