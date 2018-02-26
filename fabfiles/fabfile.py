#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement
from fabric.api import *
from fabric.network import ssh

from student_ips import IPS, PASSWORD, test_ip, test_user
from annotation import annotation, pan_genome
from assembly import assembly, assembly_qc, assembly_extras
from metagenomics import binning, metabarcoding, kraken, checkm
from rna import quant

env.hosts = IPS
env.user = 'student'
env.key_filename = '~/.ssh/proj_rsa'

# test vm
# env.hosts = test_ip
# env.user = test_user

FASTQC_WEB = 'https://launchpad.net/ubuntu/+archive/primary/+files/'
FASTQC_DEB = 'fastqc_0.11.5+dfsg-3_all.deb'

BOWTIE2_WEB = 'https://github.com/BenLangmead/bowtie2/releases/download/'
BOWTIE2_FILE = 'v2.3.4/bowtie2-2.3.4-linux-x86_64.zip'
SAMTOOLS_WEB = 'https://github.com/samtools/samtools/releases/download/'
SAMTOOLS_FILE = '1.6/samtools-1.6.tar.bz2'

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
    run('mkdir -p /home/$(whoami)/.local/share')
    run('mkdir -p /home/$(whoami)/.local/lib')


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
        sudo('rm -rf *')


def full_cleanup():
    cleanup()
    sudo('rm -rf ~/.local/')
    run('mkdir -p /home/$(whoami)/.local/bin')
    run('mkdir -p /home/$(whoami)/.local/share')
    setup()


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
