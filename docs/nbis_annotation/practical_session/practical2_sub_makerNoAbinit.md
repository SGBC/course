# Making an evidence based annotation with MAKER

## Overview

The first run of Maker will be done without ab-initio predictions. What are your expectations for the resulting gene build? In essence, we are attempting a purely evidence-based annotation, where the best protein- and EST-alignments are chosen to build the most likely gene models. The purpose of an evidence-based annotation is simple. Basically, you may try to annotate an organism where no usable ab-initio model is available. The evidence-based annotation can then be used to create a set of genes on which a new model could be trained on (using e.g. Snap or Augustus). Selection of genes for training can be based on the annotation edit distance (AED score), which says something about how great the distance between a gene model and the evidence alignments is. A score of 0.0 would essentially say that the final model is in perfect agreement with the evidence.

Let's do this step-by-step:

## Prepare the folder and input data

Create the folder where we will launch this maker run.

```
cd ~/annotation_course/practical2/maker/
mdkir evidence
cd evidence
```

Link the raw computes you want to use into your folder. The files you will need are:

- the gff file of the pre-computed repeats (coordinates of repeatmasked regions)

```
ln -s ~/annotation_course/data/raw_computes/repeatmasker.genome.gff
ln -s ~/annotation_course/data/raw_computes/repeatrunner.genome.gff
```

In addition, you will also need the genome sequence.
```
ln -s ~/annotation_course/data/genome/genome.fa
```
Then you will also need EST and protein fasta file:  
```
ln -s ~/annotation_course/data/evidence/est.genome.fa 
ln -s ~/annotation_course/data/evidence/proteins.genome.fa
```
To finish you will could use a transcriptome assembly (This one has been made using Stringtie):
```
ln -s ~/annotation_course/data/RNAseq/stringtie/stringtie2genome.genome.gff
```

/!\\ Always check that the gff files you provides as protein or EST contains match/match_part (gff alignment type ) feature types rather than genes/transcripts (gff annotation type) otherwise MAKER will not use the contained data properly. Here we have to fix the stringtie gff file.

```
gff3_sp_alignment_output_style.pl --gff stringtie2genome.genome.gff -o stringtie2genome.genome.ok.gff
```

You should now have 2 repeat files, 1 EST file, 1 protein file, 1 transcript file, and the genome sequence in the working directory. 

For Maker to use this information, we need create the three config files, typing this command:
```
maker -CTL
```

You can leave the two files controlling external software behaviors untouched. In the actual maker options file called **maker_opts.ctl**, we need to provide:

- name of the genome sequence (genome=)
- name of the 'EST' file in fasta format  (est=)
- name of the 'Transcript' file in gff format (est_gff=)
- name of the 'Protein' set file(s) (protein=)
- name of the repeatmasker and repeatrunner files (rm_gff=) 

You can list multiple files in one field by separating their names by a **comma** ','.

This time, we do not specify a reference species to be used by augustus, which will disable ab-initio gene finding. Instead we set:
  
  <i>protein2genome=1</i>  
  <i>est2genome=1</i>

This will enable gene building directly from the evidence alignments.

To edit the **maker_opts.ctl** file you can use the nano text editor:
```
nano maker_opts.ctl
```

Before running MAKER you can check you have modified the maker_opts.ctl file properly [here](practical2_supl_maker.md).<br/>
/!\ Be sure to have deactivated the parameters **model\_org= #** and **repeat\_protein= #** to avoid the heavy work of repeatmasker.

## Run Maker

If your maker\_opts.ctl is configured correctly, you should be able to run maker:
```
mpiexec -n 8 maker
```
This will start Maker on 8 cores, if everything is configured correctly.
This will take a little while and process a lot of output to the screen. Luckily, much of the heavy work - such as repeat masking - are already done, so the total running time is quite manageable, even on a small number of cores.

## Inspect the output (optional)

[Here you can find details about the MAKER output.](practical2_supl2_maker.md)

## Compile the output

Once Maker is finished, compile the annotation:
```
maker_merge_outputs_from_datastore.pl --output maker_no_abinitio
```
We have specified a name for the output directory since we will be creating more than one annotation and need to be able to tell them apart.  

This should create a "maker\_no\_abinitio" directory containing a maker annotation file together with the matching protein predictions file and a sub-directory containing different annotation files including the **maker.gff** which is the result to keep from this analysis. 

=> You could sym-link the maker.gff file to another folder called e.g. dmel\_results, so everything is in the same place in the end. Just make sure to call the link something other than maker.gff, since any maker output will be called that.


## Inspect the gene models

To get some statistics of your annotation you could launch :
```
gff3_sp_statistics.pl --gff maker_no_abinitio/annotationByType/maker.gff
```

We could now also visualise the annotation in the Webapollo genome browser.
