#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement

from fabric.api import *
from fabric.network import ssh

from student_ips import IPS, PASSWORD, test_ip, test_user

from qc import qc
from alignment import alignment
from rna import quant, rna_assembly
from annotation import annotation, pan_genome, euk_annot, functional_annot
from assembly import assembly, assembly_qc, assembly_extras
from metagenomics import binning, metabarcoding, kraken, checkm

env.hosts = IPS
env.user = 'student'
env.key_filename = '~/.ssh/azure_rsa'

# test vm
# env.hosts = '40.71.27.91'
# env.hosts = test_ip
# env.user = test_user
# env['sudo_prefix'] += '-E '

RSTUDIO_WEB = 'https://download2.rstudio.org/'
RSTUDIO_FILE = 'rstudio-server-1.0.143-amd64.deb'

KEY_SERVER = 'keyserver.ubuntu.com'
KEY = 'E298A3A825C0D65DFD57CBB651716619E084DAB9'
REPO = 'https://cran.rstudio.com/bin/linux/ubuntu'


def host_type():
    run('uname')


def passwd():
    sudo('echo "student:%s" | sudo chpasswd' % PASSWORD)


def format_sdc():
    with warn_only():
        sudo('(echo n; echo p; echo 1; echo ; echo ; echo w) | sudo fdisk /dev/sdc')
        sudo('mkfs -t ext4 /dev/sdc1')
        sudo('mount /dev/sdc1 /opt')


@parallel
def setup():
    sudo('apt -y -qq update && apt -y -qq upgrade')
    sudo('apt -y -qq install python-pip python-dev')
    sudo('apt -y -qq install unzip')
    sudo('apt -y -qq install make gcc git')
    sudo('apt -y -qq install default-jre')
    sudo('apt -y -qq install libncurses5-dev libbz2-dev liblzma-dev')
    sudo('apt -y -qq install zlib1g-dev libcurl4-gnutls-dev')
    run('mkdir -p ~/install')
    run('mkdir -p /home/$(whoami)/.local/bin')
    run('mkdir -p /home/$(whoami)/.local/share')
    run('mkdir -p /home/$(whoami)/.local/lib')


@parallel
def rstudio():
    sudo('apt-key adv --keyserver %s --recv-keys %s' % (KEY_SERVER, KEY))
    sudo('add-apt-repository "deb [arch=amd64,i386] %s xenial/"' % REPO)
    sudo('apt-get update')
    sudo('apt -y -qq install --allow-unauthenticated r-base r-base-dev')
    sudo('apt -y -qq install --allow-unauthenticated libxml2-dev libssl-dev')
    sudo('apt -y -qq install --allow-unauthenticated libcurl4-openssl-dev')
    sudo('apt -y -qq install gdebi-core')
    with cd('~/install'):
        run('wget --quiet %s%s' % (RSTUDIO_WEB, RSTUDIO_FILE))
        sudo('gdebi -n %s' % RSTUDIO_FILE)


def cleanup():
    with cd('~/install'):
        sudo('rm -rf *')


def full_cleanup():
    cleanup()
    sudo('rm -rf ~/.local/')
    run('mkdir -p /home/$(whoami)/.local/bin')
    run('mkdir -p /home/$(whoami)/.local/share')
    setup()
