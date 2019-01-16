# Assembly Challenge

During this session, you will be asked to produce the best assembly possible of *Mycoplasma * JCVI-syn1.0 Delta1-6 8-Deletion Strain.

The data comes from a synthetic genome developped by the JCVI


There are various assemblers already installed on your virtual machines but feel free to try and install others.
Below you will find the commands needed to download the data, as well as links to the websites of some well-known assemblers and quality assessment tools.

Good luck!

## Download the Data

```bash
fastq-dump -split-files SRR1530976
```

## Assemblers available

* [megahit](https://github.com/voutcn/megahit)
* [SPAdes](http://cab.spbu.ru/software/spades/)
* [sga](https://github.com/jts/sga)
* [Abyss](https://github.com/bcgsc/abyss)
* [Unicycler](https://github.com/rrwick/Unicycler)

## Quality assessment

* [quast](http://quast.sourceforge.net)
* [busco](http://busco.ezlab.org/v2/)
* [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)
* [multiqc](http://multiqc.info)
