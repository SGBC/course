#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement
from fabric.api import *
from fabric.network import ssh

from student_ips import IPS

env.hosts = IPS
env.user = 'student'
env.key_filename = '~/.ssh/azure_rsa'

FASTQC_WEB = 'https://launchpad.net/ubuntu/+archive/primary/+files/'
FASTQC_DEB = 'fastqc_0.11.5+dfsg-3_all.deb'

QUAST = 'https://github.com/ablab/quast/archive/quast_4.6.2.tar.gz'
PILON_WEB = 'https://github.com/broadinstitute/pilon/releases/download/'
PILON_FILE = 'v1.22/pilon-1.22.jar'

BOWTIE2_WEB = 'https://github.com/BenLangmead/bowtie2/releases/download/'
BOWTIE2_FILE = 'v2.3.4/bowtie2-2.3.4-linux-x86_64.zip'
SAMTOOLS_WEB = 'https://github.com/samtools/samtools/releases/download/'
SAMTOOLS_FILE = '1.6/samtools-1.6.tar.bz2'


def host_type():
    run('uname')


def profile():
    run('source ~/.bashrc')


@parallel
def setup():
    sudo('apt -y -qq update  && apt -y -qq upgrade')
    sudo('apt -y -qq install python-pip python-dev')
    sudo('apt -y -qq install unzip')
    sudo('apt -y -qq install make gcc')
    sudo('apt -y -qq install default-jre')
    sudo('apt -y -qq install libncurses5-dev libbz2-dev liblzma-dev')
    sudo('apt -y -qq install zlib1g-dev libcurl4-gnutls-dev')
    run('mkdir -p ~/install')
    run('mkdir -p /home/$(whoami)/.local/bin')


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


@parallel
def assembly():
    # megahit
    with cd('~/install'):
        run('git clone -q https://github.com/voutcn/megahit.git')
    with cd('~/install/megahit'):
        run('make')
    run('mv ~/install/megahit/megahit /home/$(whoami)/.local/bin/')
    run('mv ~/install/megahit/megahit_asm_core /home/$(whoami)/.local/bin/')
    run('mv ~/install/megahit/megahit_toolkit /home/$(whoami)/.local/bin/')

    # quast
    with cd('~/install'):
        run('wget --quiet %s' % QUAST)
        run('tar xzf quast_4.6.2.tar.gz')
    with cd('~/install/quast-quast_4.6.2'):
        sudo('./setup.py install')

    # pilon
    with cd('~/install'):
        run('wget --quiet %s%s' % (PILON_WEB, PILON_FILE))
    sudo('mkdir -p /opt/pilon')
    sudo('mv ~/install/pilon-1.22.jar /opt/pilon/pilon.jar')
    run('echo -e \'#!bin/bash\njava -jar /opt/pilon/pilon.jar $@\n\' > pilon')
    run('mv pilon /home/$(whoami)/.local/bin/')


@parallel
def alignment():
    # bowtie2
    with cd('~/install'):
        run('wget --quiet %s%s' % (BOWTIE2_WEB, BOWTIE2_FILE))
        run('unzip -q bowtie2-2.3.4-linux-x86_64.zip')
    with cd('~/install/bowtie2-2.3.4-linux-x86_64'):
        run('mv bowtie2* /home/$(whoami)/.local/bin/')
    # samtools
    with cd('~/install'):
        run('wget --quiet %s%s' % (SAMTOOLS_WEB, SAMTOOLS_FILE))
        run('tar xjf samtools-1.6.tar.bz2')
    with cd('~/install/samtools-1.6'):
        run('./configure --quiet')
        run('make')
        sudo('make install')


def cleanup():
    with cd('~/install'):
        run('rm -rf fastqc*')
        run('rm -rf scythe')
        run('rm -rf sickle')
        run('rm -rf megahit')
        sudo('rm -rf quast*')
        run('rm -rf bowtie2-2.3.4*')
        run('rm -rf samtools-1.6*')
