#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''fabric rules for deployment of annotation and pan-genome lesson'''

from __future__ import print_function, with_statement
from fabric.api import *

from student_ips import repbase_id

MAKER_WEB = 'http://yandell.topaz.genetics.utah.edu/maker_downloads/'
MAKER_ID = '7BEA/4A9C/5429/0A096F68E607BF466D5703078010/'
MAKER_FILE = 'maker-2.31.9.tgz'

REPEATMASKER_WEB = 'http://www.repeatmasker.org/'
REPEATMASKER_FILE = 'RepeatMasker-open-4-0-7.tar.gz'
REPBASE_WEB = 'https://www.girinst.org/server/RepBase/protected/'
REPBASE_FILE = 'RepBase24.01.fasta.tar.gz'


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


@parallel
def euk_deps():
    sudo('apt -y -qq install cpanminus ncbi-blast+ snap-aligner hmmer')
    sudo('apt -y -qq install exonerate openmpi-bin libmpich-dev')
    sudo('cpanm -f DBI DBD::SQLite forks forks::shared File::Which IO::All')
    sudo('cpanm -f Perl::Unsafe::Signals Bit::Vector Inline::C IO::Prompt')
    sudo('cpanm -f Text::Soundex Statistics::R LWP::UserAgent')
    sudo('cpanm -f Bio::Perl')


@parallel
def euk_progs():
    # trf
    with cd('~/install'):
        run('wget --quiet http://tandem.bu.edu/trf/downloads/trf409.linux64')
        run('chmod +x trf409.linux64')
        sudo('mv trf409.linux64 /opt/sw/bin/trf')
    # repeatmasker
    with cd('/opt/sw/share'):
        sudo('wget --quiet %s%s' % (REPEATMASKER_WEB, REPEATMASKER_FILE))
        sudo('tar xzf %s' % REPEATMASKER_FILE)
    with cd('/opt/sw/share/RepeatMasker'):
        sudo('curl -O -u %s %s%s' % (repbase_id, REPBASE_WEB, REPBASE_FILE))
        sudo('tar xzf %s' % REPBASE_FILE)
        sudo('printf "\nenv\n\n/opt/sw/bin/trf\n4\n/usr/bin\nY\n5\n" | perl ./configure')
    run('echo "export PATH=$PATH:/opt/sw/share/RepeatMasker" >> ~/.bashrc')


@parallel
def maker():
    with cd('/opt/sw/share'):
        sudo('wget --quiet %s%s%s' % (MAKER_WEB, MAKER_ID, MAKER_FILE))
        sudo('tar -xzf %s' % MAKER_FILE)
    with cd('/opt/sw/share/maker/src'):
        sudo('printf "Y\n\n\n" | perl Build.PL')
        sudo('./Build install')
    run('echo "export PATH=$PATH:~/opt/sw/share/maker/bin/" >> ~/.bashrc')


@parallel
def gaas():
    sudo('cpanm -f Moose Clone Graph::Directed')
    with cd('/opt/sw'):
        sudo('git clone https://github.com/NBISweden/GAAS.git')
    run('echo "export PERL5LIB=$PERL5LIB:/opt/sw/GAAS/annotation" >> ~/.bashrc')
    run('echo "export PATH=$PATH:/opt/sw/GAAS/annotation/Tools/Maker/:/opt/sw/GAAS/annotation/Tools/Util/gff/:/opt/sw/GAAS/annotation/Tools/Util/fasta/:/opt/sw/GAAS/annotation/Tools/Util/:/opt/sw/GAAS/annotation/Tools/Converter/" >> ~/.bashrc')


@parallel
def functional_annot():
    with cd('/opt/sw'):
        sudo('wget --quiet ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.27-66.0/interproscan-5.27-66.0-64-bit.tar.gz')
        sudo('tar pxzf interproscan-5.27-66.0-64-bit.tar.gz')
    # with cd('/opt/interproscan-5.27-66.0/data'):
        # sudo('wget --quiet ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/data/panther-data-12.0.tar.gz')
        # sudo('tar pxzf panther-data-12.0.tar.gz')
    # run('echo "export PATH=$PATH:/opt/sw/interproscan-5.27-66.0" >> ~/.bashrc')
