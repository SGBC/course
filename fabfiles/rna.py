#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement
from fabric.api import *

'''fabric rules for deployment of rna-seq lessons'''

SALMON_WEB = 'https://github.com/COMBINE-lab/salmon/releases/download/v0.9.1/'
SALMON_FILE = 'Salmon-0.9.1_linux_x86_64.tar.gz'
SALMON_DIR = 'Salmon-latest_linux_x86_64'

KEY_SERVER = 'keyserver.ubuntu.com'
KEY = 'E298A3A825C0D65DFD57CBB651716619E084DAB9'
REPO = 'https://cran.rstudio.com/bin/linux/ubuntu'


@parallel
def quant():
    # salmon
    with cd('~/install'):
        run('wget --quiet %s%s' % (SALMON_WEB, SALMON_FILE))
        run('tar xzf %s' % SALMON_FILE)
    run('mv ~/install/%s/bin/* ~/.local/bin/' % SALMON_DIR)
    run('mv ~/install/%s/lib/* ~/.local/lib/' % SALMON_DIR)

    # r packages
    sudo('apt-key adv --keyserver %s --recv-keys %s' % (KEY_SERVER, KEY))
    sudo('add-apt-repository "deb [arch=amd64,i386] %s xenial/"' % REPO)
    sudo('apt-get update')
    sudo('apt -y -qq install --allow-unauthenticated r-base r-base-dev')
    sudo('apt -y -qq install --allow-unauthenticated libxml2-dev libssl-dev')
    sudo('apt -y -qq install libmariadb-client-lgpl-dev')
    sudo('apt -y -qq install --allow-unauthenticated libcurl4-openssl-dev')
    with cd('~/install'):
        run('curl -O -J -L https://osf.io/a7kqz/download')
        sudo('Rscript install.R')
