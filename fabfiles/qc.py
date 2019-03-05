#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement
from fabric.api import *

'''fabric rules for deployment of qc lesson'''


@parallel
def qc():
    # fastqc
    run("~/miniconda3/bin/conda install -y fastqc sickle-trim multiqc")
