from __future__ import print_function, with_statement
from fabric.api import *

'''fabric rules for deployment of alignment software'''


@parallel
def alignment():
    run("~/miniconda3/bin/conda install -y bowtie2 bwa samtools")
