#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement

from fabric.api import *
from fabric.network import ssh

from student_ips import IPS, PASSWORD

from qc import qc
from alignment import alignment
from rna import quant, rna_assembly
from annotation import annotation, pan_genome, euk_deps, euk_progs, maker, gaas, functional_annot
from assembly import assembly
from metagenomics import binning, metabarcoding, kraken, checkm

env.hosts = IPS
env.user = 'student'
env.key_filename = '~/.ssh/azure_2019.rsa'

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


@parallel
def mount():
    sudo("mount /dev/sdc1 /opt")


@parallel
def format_sdc():
    with warn_only():
        sudo('(echo n; echo p; echo 1; echo ; echo ; echo w) | sudo fdisk /dev/sdc')
        sudo('mkfs -t ext4 /dev/sdc1')
        # sudo('mount /dev/sdc1 /opt')


@parallel
def conda():
    run("wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh")
    run("bash Miniconda3-latest-Linux-x86_64.sh -b -f")
    run("rm Miniconda3-latest-Linux-x86_64.sh")
    run('echo "export PATH=$PATH:~/miniconda3/bin" >> ~/.bashrc')
    run("~/miniconda3/bin/conda config --add channels defaults")
    run("~/miniconda3/bin/conda config --add channels bioconda")
    run("~/miniconda3/bin/conda config --add channels conda-forge")


@parallel
def setup():
    #     format_sdc()
    mount()
    sudo('apt -y -qq install python-pip python-dev')
    sudo('apt -y -qq install unzip')
    sudo('apt -y -qq install make gcc git')
    sudo('apt -y -qq install default-jre')
    sudo('apt -y -qq install libncurses5-dev libbz2-dev liblzma-dev')
    sudo('apt -y -qq install zlib1g-dev libcurl4-gnutls-dev')
    run('mkdir -p ~/install')
    sudo('mkdir -p /opt/sw/bin')
    sudo('mkdir -p /opt/sw/share')
    sudo('mkdir -p /opt/sw/lib')


@parallel
def r():
    sudo('apt-get update')
    sudo('apt -y -qq install --allow-unauthenticated r-base r-base-dev')
    sudo('apt -y -qq install --allow-unauthenticated libxml2-dev libssl-dev')
    sudo('apt -y -qq install --allow-unauthenticated libcurl4-openssl-dev')
#     sudo('apt -y -qq install gdebi-core')
#     with cd('~/install'):
#         run('wget --quiet %s%s' % (RSTUDIO_WEB, RSTUDIO_FILE))
#         sudo('gdebi -n %s' % RSTUDIO_FILE)


@parallel
def cleanup():
    with cd('~/install'):
        sudo('rm -rf *')


def full_cleanup():
    cleanup()
    sudo('rm -rf /opt/sw/*')
    setup()
