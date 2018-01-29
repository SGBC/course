#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement
from fabric.api import *
from fabric.network import ssh

from student_ips import IPS

env.hosts = IPS
env.user = 'student'
env.key_filename = '~/.ssh/azure_rsa'


FASTQC_WEB = 'https://www.bioinformatics.babraham.ac.uk/'
FASTQC_FILE = 'projects/fastqc/fastqc_v0.11.7.zip'


def host_type():
    run('uname -a')


def get_path():
    run('echo $PATH')


@parallel
def setup():
    sudo('apt -y -qq update  && apt -y -qq upgrade')
    sudo('apt -y -qq install python-pip python-dev')
    sudo('apt -y -qq install unzip')
    sudo('apt -y -qq install make gcc')
    sudo('apt -y -qq install libncurses5-dev libbz2-dev liblzma-dev')
    sudo('apt -y -qq install zlib1g-dev libcurl4-gnutls-dev')
    run('mkdir -p ~/install')
    run('mkdir -p /home/$(whoami)/.local/bin')


@parallel
def qc():
    # fastqc
    with cd('~/install'):
        run('wget --quiet %s%s' % (FASTQC_WEB, FASTQC_FILE))
        run('unzip -q fastqc_v0.11.7.zip')
        run('chmod +x FastQC/fastqc')
        run('mv FastQC/fastqc /home/$(whoami)/.local/bin')

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


def cleanup():
    with cd('~/install'):
        run('rm -rf fastqc_v0.11.7.zip')
        run('rm -rf FastQC')
        run('rm -rf scythe')
        run('rm -rf sickle')