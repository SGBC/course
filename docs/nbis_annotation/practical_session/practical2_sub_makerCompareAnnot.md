# Comparing and evaluating annotations

## Prerequisites  

First create the folder where yo will work:  
```
cd ~/annotation_course/practical2
mkdir assess
cd assess
```

In this exercise you will handle different annotation files: 

 * the pure abinitio one done with augustus (practical1),
 ```
 ln -s ~/annotation_course/practical1/augustus/augustus_drosophila.gff 
 ```

 * the evidence-based done with MAKER
  ```
 ln -s ../maker/maker_evidence/maker.gff maker_evidence.gff 
 ```
 
 * the abinitio evidence drived one done with MAKER.
  ```
 ln -s ../maker/maker_abinitio/maker.gff maker_abinitio.gff
 ```
 
 * the official annotation from Ensembl
  ```
 ln -s ~/annotation_course/data/annotation/ensembl.genome.gff
 ```
 
 First, we will count the features annotated in each of them and compare that number against the existing reference annotation. Next, we will perform a proper feature-level comparison to obtain a proper estimate of congruency.

## Evaluating annotation quality

Evaluating an annotation can be done in different ways:

 * looking at the number of genes  
It isn't so much a quality check as a measure of congruency - i.e. the resulting numbers don't tell you which of the two gene builds is more correct.

 * comparison with another annotation  
 It doesnät help neither to see the quality of your annotaiton but could help to understand the major differences between several annotation.

 * running busco on proteins obtained from the annotation  
 It provides a nice feeling about the quality of the annotaiton but is biasied by the fact it focus only on well conserved genes between sepeceis during evolution. So, what about species specific genes ?
 
 * in reference to the evidence alignments (AED score)  
 It is what Maker uses internally to select gene models. After synthesizing and annotating loci, the resulting model will be ranked against the filtered evidence alignments. The more congruent these two points of information are, the lower the 'annotation edit distance' (AED) will be. The AED score can be used to e.g. check an annotation for problematic models that may then be subjected to manual curation.

### BUSCO

BUSCO is run before annotating to check if the assembly is good and therefore if the annotation will be good. It is also run after the structural annotation to then compare if we indeed find a number of genes corresponding of the first run of busco.

You will need to link the protein file created by maker on the run with the ab-initio
```
cd ~/annotation_course/practical2
mkdir busco
cd busco

ln -s ../maker/maker_abinitio/genome.all.maker.proteins.fasta
ln -s ~/annotation_course/practical1/busco/metazoa_odb9

BUSCO.py -i genome.all.maker.proteins.fasta -o dmel_maker_abinitio -m prot -c 8 -l metazoa_odb9
```
- if you compare with you first busco results what do you see?

## Comparing annotations

As with many tasks within bioinformatics, it is always a great idea to first look around for existing solutions. In the case of comparing annotations, there are in fact options already out there. One such example is genometools, which we have briefly used before.


### Preparing the input files
First you have to be situated in a folder containing the two maker annotations (with and without ab initio) and the augustus annotation. 
```
cd ~/annotation_course/practical2
mkdir compare
cd compare
```

Then, copy or sym-link the EnsEMBL reference annotation.
```
ln -s ~/annotation_course/data/annotation/ensembl.genome.gff
```

Now we have to sort any GFF3-formatted annotation in a way that genometools accepts.
```
sed -i '1i##gff-version 3' maker_evidence.gff
sed -i '1i##gff-version 3' maker_abinitio.gff

gt gff3 -sort maker_evidence.gff > maker_evidence.sorted.gff 
gt gff3 -sort maker_abinitio.gff > maker_abinitio.sorted.gff 
gt gff3 -sort ensembl.genome.gff > ensembl.sorted.gff 
```

### Counting features

Next, we get the feature counts for the three annotations and the reference from EnsEMBL:
```
gt stat maker_no_abinitio.gff
```
or
```
gff3_sp_statistics.pl --gff maker_no_abinitio.gff
```

(or whatever you decided to name the file(s). The use of the sorted file or the original one changes nothing here)

As you will note, there are some differences - and of course, this is expected, since we used quite different approaches to generate the two gene builds. EnsEMBL on the other hand is originally imported from FlyBase. Obviously, a lot of manual labor and much more data has been put into the FlyBase annotation - and this highlights a common limitation of any computational pipeline. You will simply never reach the same level of quality and detail as seen in a manually curated reference annotation.

### Pairwise comparison of features

But feature counts alone can't really give you a clear measure of overlap/differences between any two annotations. In order to properly compare them, we can use another function included in genometools.

With the sorted files, we can now perform a comparison:
```
gt eval ensembl.sorted.gff maker_evidence.sorted.gff
```
This will create a long list of measures for all relevant sequence features with respect to both the 'sensitivity' and 'specificity' - as a measure of how close the annotation comes to a reference. As a reminder, 'specificity' measures the fraction of a reference overlapping a prediction whereas 'sensitivity' measures the fraction of a prediction overlapping a reference.

Note that the measures employed by genometools function in a all-or-nothing fashion. If the overlap is not 100%, it doesn't count (which is why you are unlikely to find gene-level congruencies between your gene builds and the reference annotation).  

From the comparison of your annotations to the Ensembl annotation, which one **seems** to be the most comprehensive to you ?

## Visualising annotations

**Note:** The following section overlaps with some of the exercises you have done earlier (comparing augustus predictions against the reference annotation).

In the previous tasks, we have looked at the overlap between different gene builds. While this gives us an indication of how similar two annotations are, **it doesn't really allow us to judge the overall quality and similarity of annotations**. Remember, sensitivity and specificity are 'all-or-nothing' - two annotations may be considered very different, but provide similar information, biologically. By that, we mean that two gene models don't need to be 100% identical in their coordinates to tell the scientist that a gene indeed exists in a given location and what it's product looks like.

We therefore need to visually inspect and compare the gene builds. This is a crucial step in any annotation project - gene build pipelines use a set of defined rules, but human pattern recognition is needed to spot potential systematic errors. For example, a pipeline like Maker will simply take all your input and try to synthesize it into an annotation, but it doesn't do too much checks on the data itself. What if you RNA-seq data is messier than you thought? What if your protein data set includes to many 'predicted' proteins that are in clear conflict with the other data?

There exist a number of 'annotation viewers' - IGV, Argo and Apollo, to name a few. A common choice for annotators is the web-based version of Apollo, WebApollo, mostly for its curation capabilities.

### Using WebApollo to view annotations
Transfer your maker annotation files to your computer using the scp command.  
Then, jump to [WebApollo](http://annotation-prod.scilifelab.se:8080/NBIS_course/) and upload your annotation track into the genome portal called **drosophila\_melanogaster\_chr4**. [Here find the WebApollo instruction](UsingWebapollo)  
You can now compare your gene builds against this reference. Some questions to ask yourself:

- Do my gene builds recover all the genes found in the reference?  
- What sort of differences are most common?  
