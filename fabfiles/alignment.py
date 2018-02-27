from __future__ import print_function, with_statement
from fabric.api import *

'''fabric rules for deployment of alignment software'''

BOWTIE2_WEB = 'https://github.com/BenLangmead/bowtie2/releases/download/'
BOWTIE2_FILE = 'v2.3.4/bowtie2-2.3.4-linux-x86_64.zip'
SAMTOOLS_WEB = 'https://github.com/samtools/samtools/releases/download/'
SAMTOOLS_FILE = '1.6/samtools-1.6.tar.bz2'


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
        run('make --quiet')
        sudo('make --quiet install')
