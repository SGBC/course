#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''fabric rules for deployment of metagenomics lessons'''

from __future__ import print_function, with_statement
from fabric.api import *

METABAT_WEB = 'https://bitbucket.org/berkeleylab/metabat/downloads/'
METABAT_FILE = 'metabat-static-binary-linux-x64_v2.12.1.tar.gz'
METABAT_DIR = 'metabat'

PRODIGAL_WEB = 'https://github.com/hyattpd/Prodigal/releases/download/v2.6.3/'
PRODIGAL_FILE = 'prodigal.linux'
PPLACER_WEB = 'https://github.com/matsen/pplacer/releases/download/v1.1.alpha17/'
PPLACER_FILE = 'pplacer-Linux-v1.1.alpha17.zip'
PPLACER_DIR = 'pplacer-Linux-v1.1.alpha17'

CHECKM_DB_WEB = 'https://data.ace.uq.edu.au/public/CheckM_databases/'
CHECKM_DB_FILE = 'checkm_data_2015_01_16.tar.gz'
CHECKM_DB_DIR = '~/.local/data/checkm'


def binning():
    # metabat
    with cd('~/install'):
        run('wget --quiet %s%s' % (METABAT_WEB, METABAT_FILE))
        run('tar xzf %s' % METABAT_FILE)
    run('rm ~/install/%s/*.txt' % METABAT_DIR)
    run('rm ~/install/%s/*.md' % METABAT_DIR)
    run('mv ~/install/%s/* ~/.local/bin/' % METABAT_DIR)

    # checkm
    sudo('apt install -y -qq hmmer')
    with cd('~/install'):
        run('wget --quiet %s%s' % (PRODIGAL_WEB, PRODIGAL_FILE))
        run('chmod +x %s' % PRODIGAL_FILE)
    run('mv ~/install/%s ~/.local/bin/prodigal' % PRODIGAL_FILE)
    with cd('~/install'):
        run('wget --quiet %s%s' % (PPLACER_WEB, PPLACER_FILE))
        run('unzip -q %s' % PPLACER_FILE)
    with cd('~/install/%s' % PPLACER_DIR):
        run('mv guppy pplacer rppr ~/.local/bin/')
    sudo('pip install -q numpy')
    sudo('pip install -q checkm-genome')

    # checkm cannot set data root non-interactively
    # waiting for upstream fix

    # run('mkdir -p ~/.local/data/checkm')
    # with cd('%s' % CHECKM_DB_DIR):
    #     run('wget --quiet %s%s' % (CHECKM_DB_WEB, CHECKM_DB_FILE))
    #     run('tar xzf %s' % CHECKM_DB_FILE)
    # sudo('checkm data setRoot %s' % CHECKM_DB_DIR)
