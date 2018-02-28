## Inspect the output

### Finding your way around

By default, Maker will write the output of its different analyses into a folder named:

&lt;name\_of\_genome\_fasta&gt;.maker.output

In our case:

 4.maker.output

Within the main output directory, Maker keeps a copy of the config files, a database (here: 4.db), directories for the blast databases created from your evidence data and a file called 4\_master\_datastore\_index.log.

Out of these files, only the 4\_master\_datastore\_index is really interesting to us. It includes a log of all the contigs included in the genome fasta file - together with their processing status (ideally: FINISHED) and the location of the output files. Since Maker can technically run in parallel on a large number of contigs, it creates separate folders for each of these input data. For larger genomes, this can generate a very deep and confusing folder tree. The 4\_master\_datastore\_index helps you make sense of it:

4       4\_datastore/A8/7F/4/ STARTED  
4       4\_datastore/A8/7F/4/ FINISHED

This meens the sequence **4** was started - and finished, with all data (annotation, protein predictions etc) written to the subfolder 4\_datastore/A8/7F/4/.

If you look into that folder, you will find the finished Maker annotation for this contig.

rw-rw-r- 1 student student 472193 Mar 24 10:16 4.gff  
\*rw-rw-r- 1 student student 3599 Mar 24 10:16 4.maker.augustus\_masked.proteins.fasta 
\*rw-rw-r- 1 student student 10388 Mar 24 10:16 4.maker.augustus\_masked.transcripts.fasta  
\*rw-rw-r- 1 student student 176 Mar 24 10:16 4.maker.non\_overlapping\_ab\_initio.proteins.fasta
\*rw-rw-r- 1 student student 328 Mar 24 10:16 4.maker.non\_overlapping\_ab\_initio.transcripts.fasta  
rw-rw-r- 1 student student 3931 Mar 24 10:16 4.maker.proteins.fasta  
rw-rw-r- 1 student student 20865 Mar 24 10:16 4.maker.transcripts.fasta  
rw-rw-r- 1 student student 4248 Mar 24 10:15 run.log  
drwxrwsr-x 3 student student 4096 Mar 24 10:16 theVoid.4

\* only if an abinitio tool has been activated

The main annotation file is '4.gff' - including both the finished gene models and all the raw compute data. The other files include fasta files for the different sequence features that have been annotated - based on ab-initio predictions through augustus as well as on the finished gene models. The folder 'theVoid' include all the raw computations that Maker has performed to synthesize the evidence into gene models.

## Understanding a Maker annotation

You have two options now for gathering the output in some usable form - copy select files by hand to wherever you want them. Or you can use a script that does the job for you (we have included an example in the script folder).

From the folder you have run Maker, run the script called 'maker\_merge\_outputs\_from\_datastore' to create an output file for all annotations and protein files:
```
maker_merge_outputs_from_datastore.pl 
```
This will create a directory called "annotations" containing:

\-annotations.gff  
\-annotations.proteins.fa  
\-annotationByType/  

 - ***annotations.gff* file**  

If you use 'less' to read the annotation file *annotations.gff* ([GFF3 format](http://www.sequenceontology.org/gff3.shtml)), you will see a range of different features:
```
##gff-version 3  
4       .       contig  1       1351857 .       .       .       ID=4;Name=4
4       maker   gene    24134   25665   .       +       .       ID=maker-4-exonerate_protein2genome-gene-0.0;Name=maker-4-exonerate_protein2genome-gene-0.0
4       maker   mRNA    24134   25665   917     +       .       ID=maker-4-exonerate_protein2genome-gene-0.0-mRNA-1;Parent=maker-4-exonerate_protein2genome-gene-0.0;Name=maker-4-exonerate_protein2genome-gene-0.0-mRNA-1;_AED=0.09;_eAED=0.09;_QI=0|0.33|0.25|1|0|0|4|44|290
```
...

For example, the above lines read:

A new contig is being shown, with the id '4' and a length of 1351857 nucleotides  
On this contig, a gene feature is located from position 24134 to 25665, on the plus strand and with the id 'maker-4-exonerate\_protein2genome-gene-0.0'. 
On this contig, belonging to the gene, is located a transcript from position 24134 to 25665, on the plus strand and with the id 'maker-4-exonerate\_protein2genome-gene-0.0-mRNA-1'. It's quality, or AED score, is 0.09 - which means that the evidence alignments are close to be in perfect agreement with the transcript model.

And so on.

 - ***annotations.proteins.fa* file**  
This file contains the proteins translated from the CDS of gene models predicted.

 - ***annotationByType* directory**  
The different types of information present in the annotation file (annotations.gff) are separated into independent file into the "annotationByType" directory. This is useful for a number of applications, like visualizing it as separate tracks in a genome browser. Or to compute some intersting numbers from the gene models.


This should contains a bunch of files, including '**maker.gff**' - which contains the actual gene models.

### Inspect the gene models

To get some statistics of your annotation you could launch :
```
gff3_sp_statistics.pl --gff maker.gff
```

We could now also visualise all this information using a genome browser, such as Webapollo or [IGV](http://software.broadinstitute.org/software/igv/). Those viewer require a genome fasta file and any number of annotation files in GTF or GFF3 format (note that GFF3 formatted file tend to look a bit weird in IGV sometimes).
