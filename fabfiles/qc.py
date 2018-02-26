#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement
from fabric.api import *

'''fabric rules for deployment of qc lesson'''

FASTQC_WEB = 'https://launchpad.net/ubuntu/+archive/primary/+files/'
FASTQC_DEB = 'fastqc_0.11.5+dfsg-3_all.deb'


@parallel
def qc():
    # fastqc
    with cd('~/install'):
        sudo('apt -y -qq install libjbzip2-java libcommons-math3-java')
        run('wget --quiet %s%s' % (FASTQC_WEB, FASTQC_DEB))
        sudo('dpkg -i fastqc_0.11.5+dfsg-3_all.deb')
        sudo('apt -y -qq install -f')

    # scythe
    with cd('~/install'):
        run('git clone -q https://github.com/vsbuffalo/scythe.git')
    with cd('~/install/scythe'):
        run('make all')
    run('mv ~/install/scythe/scythe /home/$(whoami)/.local/bin/')

    # sickle
    with cd('~/install'):
        run('git clone -q https://github.com/najoshi/sickle.git')
    with cd('~/install/sickle'):
        run('make')
    run('mv ~/install/sickle/sickle /home/$(whoami)/.local/bin/')

    # multiqc
    sudo('pip install -q multiqc')
