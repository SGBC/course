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
REPBASE_WEB = 'http://www.girinst.org/server/RepBase/protected/repeatmaskerlibraries/'
REPBASE_FILE = 'RepBaseRepeatMaskerEdition-20170127.tar.gz'


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


def euk_annot():
    sudo('apt -y -qq install cpanminus ncbi-blast+ snap-aligner hmmer')
    sudo('apt -y -qq install exonerate openmpi-bin libmpich-dev')
    sudo('cpanm -f DBI DBD::SQLite forks forks::shared File::Which IO::All')
    sudo('cpanm -f Perl::Unsafe::Signals Bit::Vector Inline::C IO::Prompt')
    sudo('cpanm -f Text::Soundex Statistics::R LWP::UserAgent')
    sudo('cpanm -f Bio::Perl')
    # trf
    with cd('~/install'):
        run('wget --quiet http://tandem.bu.edu/trf/downloads/trf409.linux64')
        run('chmod +x trf409.linux64')
        run('mv trf409.linux64 ~/.local/bin/trf')
    # repeatmasker
    with cd('~/.local'):
        run('wget --quiet %s%s' % (REPEATMASKER_WEB, REPEATMASKER_FILE))
        run('tar xzf %s' % REPEATMASKER_FILE)
    with cd('~/.local/RepeatMasker'):
        run('curl -O -u %s %s%s' % (repbase_id, REPBASE_WEB, REPBASE_FILE))
        run('tar xzf %s' % REPBASE_FILE)
        run('printf "\nenv\n\n\n4\n/usr/bin\nY\n5\n" | perl ./configure')
    run('echo "export PATH=$PATH:~/.local/RepeatMasker" >> ~/.bashrc')
    # maker
    with cd('~/.local'):
        run('wget --quiet %s%s%s' % (MAKER_WEB, MAKER_ID, MAKER_FILE))
        run('tar -xzf %s' % MAKER_FILE)
    with cd('~/.local/maker/src'):
        run('perl Build.PL')
        run('./Build install')
    run('echo "export PATH=$PATH:~/.local/maker/bin" >> ~/.bashrc')
    # GAAS
    sudo('cpanm -f Moose Clone Graph::Directed')
    with cd('~/.local'):
        run('git clone https://github.com/NBISweden/GAAS.git')
    run('echo "export PERL5LIB=$PERL5LIB:~/.local/GAAS/annotation" >> ~/.bashrc')
    run('echo "export PATH=$PATH:~/.local/GAAS/annotation/Tools/Maker/:~/.local/GAAS/annotation/Tools/Util/gff/:~/.local/GAAS/annotation/Tools/Util/fasta/:~/.local/GAAS/annotation/Tools/Util/" >> ~/.bashrc')


def functional_annot():
    with cd('/mnt'):
        sudo('wget --quiet ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.27-66.0/interproscan-5.27-66.0-64-bit.tar.gz')
        sudo('tar pxzf interproscan-5.27-66.0-64-bit.tar.gz')
    with cd('/mnt/interproscan-5.27-66.0/data'):
        sudo('wget --quiet ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/data/panther-data-12.0.tar.gz')
        sudo('tar pxzf panther-data-12.0.tar.gz')
        run('echo "export PATH=$PATH:/mnt/interproscan-5.27-66.0" >> ~/.bashrc')
