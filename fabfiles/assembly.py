#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''fabric rules for deployment of assembly lesson'''

from __future__ import print_function, with_statement
from fabric.api import *

QUAST_WEB = 'https://github.com/ablab/quast/archive/'
QUAST_FILE = 'quast_4.6.2.tar.gz'
QUAST_DIR = 'quast-quast_4.6.2'

PILON_WEB = 'https://github.com/broadinstitute/pilon/releases/download/v1.22/'
PILON_FILE = 'pilon-1.22.jar'

SPADES_WEB = 'http://cab.spbu.ru/files/release3.11.1/'
SPADES_FILE = 'SPAdes-3.11.1-Linux.tar.gz'
SPADES_DIR = 'SPAdes-3.11.1-Linux'


@parallel
def assembly():
    # megahit
    with cd('~/install'):
        run('git clone -q https://github.com/voutcn/megahit.git')
    with cd('~/install/megahit'):
        run('make')
    run('mv ~/install/megahit/megahit ~/.local/bin/')
    run('mv ~/install/megahit/megahit_asm_core ~/.local/bin/')
    run('mv ~/install/megahit/megahit_toolkit ~/.local/bin/')

    # quast
    sudo('apt -y -qq install csh libboost1.58-dev')
    with cd('~/install'):
        run('wget --quiet %s%s' % (QUAST_WEB, QUAST_FILE))
        run('tar xzf %s' % QUAST_FILE)
    with cd('~/install/%s' % QUAST_DIR):
        sudo('./setup.py install')

    # pilon
    with cd('~/install'):
        run('wget --quiet %s%s' % (PILON_WEB, PILON_FILE))
    sudo('mkdir -p /opt/pilon')
    sudo('mv ~/install/%s /opt/pilon/pilon.jar' % PILON_FILE)
    run('echo -e \'#!bin/bash\njava -jar /opt/pilon/pilon.jar $@\n\' > pilon')
    run('mv pilon ~/.local/bin/')


@parallel
def assembly_extras():
    # spades
    with cd('~/install'):
        run('wget --quiet %s%s' % (SPADES_WEB, SPADES_FILE))
        run('tar xzf %s' % SPADES_FILE)
    run('mv ~/install/%s/bin/* ~/.local/bin/' % SPADES_DIR)
    run('mv ~/install/%s/share/spades ~/.local/share/spades' % SPADES_DIR)

    # sga
    sudo('apt -y -qq install libsparsehash-dev libjsoncpp1')
    sudo('apt -y -qq install automake cmake')
    sudo('pip install -q pysam ruffus')
    with cd('~/install'):
        run('git clone -q git://github.com/pezmaster31/bamtools.git')
    with cd('~/install/bamtools'):
        run('mkdir -p build')
    with cd('~/install/bamtools/build'):
        run('cmake ..')
        run('make')
        sudo('make install')
    with cd('~/install'):
        run('git clone -q https://github.com/jts/sga.git')
    with cd('~/install/sga/src'):
        run('./autogen.sh')
        run('./configure --with-bamtools=/usr/local')
        run('make')
        sudo('make install')

    # abyss
    sudo('apt -y -qq install abyss')
