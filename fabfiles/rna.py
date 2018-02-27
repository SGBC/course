#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement
from fabric.api import *

'''fabric rules for deployment of rna-seq lessons'''

SALMON_WEB = 'https://github.com/COMBINE-lab/salmon/releases/download/v0.9.1/'
SALMON_FILE = 'Salmon-0.9.1_linux_x86_64.tar.gz'
SALMON_DIR = 'Salmon-latest_linux_x86_64'


@parallel
def quant():
    # salmon
    with cd('~/install'):
        run('wget --quiet %s%s' % (SALMON_WEB, SALMON_FILE))
        run('tar xzf %s' % SALMON_FILE)
    run('mv ~/install/%s/bin/* ~/.local/bin/' % SALMON_DIR)
    run('mv ~/install/%s/lib/* ~/.local/lib/' % SALMON_DIR)

    # r packages
    sudo('apt -y -qq install libmariadb-client-lgpl-dev')
    with cd('~/install'):
        run('curl -O -J -L https://osf.io/a7kqz/download')
        sudo('Rscript install.R')


@parallel
def rna_assembly():
    sudo('apt -y -qq install tophat jellyfish')
    with cd('~/install'):
        run('wget --quiet http://ccb.jhu.edu/software/stringtie/dl/stringtie-1.3.4c.Linux_x86_64.tar.gz')
        run('tar xzf stringtie-1.3.4c.Linux_x86_64.tar.gz')
        run('mv stringtie-1.3.4c.Linux_x86_64/stringtie ~/.local/bin')
        run('wget --quiet https://github.com/trinityrnaseq/trinityrnaseq/archive/Trinity-v2.6.5.tar.gz')
        run('tar xzf Trinity-v2.6.5.tar.gz')
    with cd('~/install/trinityrnaseq-Trinity-v2.6.5'):
        run('make')
        sudo('make install')
    run('echo "export TRINITY_HOME=/usr/local/bin/trinityrnaseq-Trinity-v2.6.5" >> ~/.bashrc')
    run('echo "export PATH=$PATH:/usr/local/bin/trinityrnaseq-Trinity-v2.6.5" >> ~/.bashrc')
