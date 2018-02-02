#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''fabric rules for deployment of annotation and pan-genome lesson'''

from __future__ import print_function, with_statement
from fabric.api import *


@parallel
def annotation():
    sudo('apt -y -qq install libdatetime-perl libxml-simple-perl \
        libdigest-md5-perl git default-jre bioperl')
    with cd('/opt'):
        sudo('git clone --quiet https://github.com/tseemann/prokka.git')
    run('echo "export PATH=$PATH:/opt/prokka/bin" >> ~/.bashrc')
    sudo('/opt/prokka/bin/prokka --setupdb')


@parallel
def pan_genome():
    # roary
    sudo('apt -y -qq install bedtools cd-hit ncbi-blast+ mcl parallel \
        cpanminus prank mafft fasttree')
    sudo('cpanm -f Bio::Roary')
