# Functional annotation

Functional annotation is the process during which we try to put names to faces - what do genes that we have annotated and curated? Basically all existing approaches accomplish this by means of similarity. If a translation product has strong similarity to a protein that has previously been assigned a function, the function in this newly annotated transcript is probably the same. Of course, this thinking is a bit problematic (where do other functional annotations come from...?) and the method will break down the more distant a newly annotated genome is to existing reference data. A complementary strategy is to scan for more limited similarity - specifically to look for the motifs of functionally characterized protein domains. It doesn't directly tell you what the protein is doing exactly, but it can provide some first indication.

In this exercise we will use an approach that combines the search for full-sequence simliarity by means of 'Blast' against large public databases with more targeted characterization of functional elements through the InterproScan pipeline. Interproscan is a meta-search engine that can compare protein queries against numerous databases. The output from Blast and Interproscan can then be used to add some information to our annotation.

## Prepare the input data

Since we do not wish to spend too much time on this, we will again limit our analysis to chromosome 4. It is also probably best to choose the analysis with ab-initio predictions enabled (unless you found the other build to be more convincing). Maker produces a protein fasta file (called "annotations.proteins.fa") together with the annotation and this file should be located in your maker directory.

Move in the proper folder:  
```
cd ~/annotation_course/practical4 
```
Now link the annotation you choose to work with. The command will looks like:
```
ln -s ~/annotation_course/practical2/maker/maker_with_abinitio/annotationByType/maker.gff maker_with_abinitio.gff  
```
Extract the corresponding proteins from the gff file:
```
ln -s ~/annotation_course/data/genome/4.fa
gff3_sp_extract_sequences.pl --gff maker_with_abinitio.gff -f 4.fa -p -o AA.fa 
```
## Interproscan approach
 Interproscan combines a number of searches for conserved motifs and curated data sets of protein clusters etc. This step may take fairly long time. It is recommended to paralellize it for huge amount of data by doing analysis of chunks of tens or hundreds proteins.

### Perform [InterproScan](https://github.com/ebi-pf-team/interproscan/wiki) analysis
InterproScan can be run through a website or from the command line on a linux server. Here we are interested in the command line approach.
<u>Interproscan allows to look up pathways, families, domains, sites, repeats, structural domains and other sequence features.</u>  

Launch Interproscan with the option -h if you want have a look about all the parameters.

- The '-app' option allows defining the database used. Here we will use the PfamA,ProDom,SuperFamily and PIRSF databases.  
- Interproscan uses an internal database that related entries in public databases to established GO terms. By running the '-goterms' option, we can add this information to our data set.
- If you enable the InterPro lookup ('-iprlookup'), you can also get the InterPro identifier corresponding to each motif retrieved: for example, the same motif is known as PF01623 in Pfam and as IPR002568 in InterPro. 
- The option '-pa' provides mappings from matches to pathway information (MetaCyc,UniPathway,KEGG,Reactome).
``` 
interproscan.sh -i maker_with_abinitio/annotations.proteins.fa -t p -dp -pa -appl Pfam,ProDom-2006.1,SuperFamily-1.75,PIRSF-3.01 --goterms --iprlookup
```
The analysis shoud take 2-3 secs per protein request - depending on how many sequences you have submitted, you can make a fairly deducted guess regarding the running time.  
You will obtain 3 result files with the following extension '.gff3', '.tsv' and '.xml'. Explanation of these output are availabke [>>here<<](https://github.com/ebi-pf-team/interproscan/wiki/OutputFormats).


### load the retrieved functional information in your annotation file:
Next, you could write scripts of your own to merge interproscan output into your annotation. Incidentially, Maker comes with utility scripts that can take InterProscan output and add it to a Maker annotation file (you need to load maker).  

- ipr\_update\_gff: adds searchable tags to the gene and mRNA features in the GFF3 files.  
- iprscan2gff3: adds physical viewable features for domains that can be displayed in JBrowse, Gbrowse, and Web Apollo.
```
ipr_update_gff maker.gff interproscan.tsv > maker.with_interpro.gff
```
Where a match is found, the new file will now include features called Dbxref and/or Ontology_term in the gene and transcript feature field (9th column).


## BLAST approach
Blast searches provide an indication about potential homology to known proteins.
A 'full' Blast analysis can run for several days and consume several GB of Ram. Consequently, for a huge amount of data it is recommended to parallelize this step doing analysis of chunks of tens or hundreds proteins. This approach can be used to give a name to the genes and a function to the transcripts.

### Perform Blast searches from the command line on Uppmax:

To run Blast on your data, use the Ncbi Blast+ package against a Drosophila-specific database (included in the folder we have provided for you, under **annotation\_course/data/blastdb/uniprot\_dmel/uniprot\_dmel.fa**) - of course, any other NCBI database would also work:
```
blastp -db ~/annotation_course/data/blastdb/uniprot_dmel/uniprot_dmel.fa -query AA.fa -outfmt 6 -out blast.out -num_threads 8
```
Against the Drosophila-specific database, the blast search takes about 2 secs per protein request - depending on how many sequences you have submitted, you can make a fairly deducted guess regarding the running time.

### Process the blast outout with Annie
The Blast outputs must be processed to retrieve the information of the closest protein (best e-value) found by Blast. This work will be done using [annie](https://github.com/genomeannotation/annie).  

First download annie:  
```
git clone https://github.com/genomeannotation/Annie.git 
```
Now launch annie: 
```
Annie/annie.py -b blast.out -db ~/annotation_course/data/blastdb/uniprot_dmel/uniprot_dmel.fa -g maker_with_abinitio.gff -o maker_annotation.annie
```

Annie writes in a 3-column table format file, providing gene name and mRNA product information. The purpose of annie is relatively simple. It recovers the information in the sequence header of the uniprot fasta file, from the best sequence found by Blast (the lowest e-value).

### load the retrieved information in your annotation file:  

Now you should be able to use the following script: 
```
~/annotation_course/course_material/git/GAAS/annotation/Tools/Maker/maker_gff3manager_JD_v8.pl -f maker.with_interpro.gff -b maker_annotation.annie -o finalOutputDir  
```
That will add the name attribute to the "gene" feature and the description attribute (corresponding to the product information) to the "mRNA" feature into you annotation file. This script may be used for other purpose like to modify the ID value by something more convenient (i.e FLYG00000001 instead of maker-4-exonerate_protein2genome-gene-8.41).  
The improved annotation is a file named "codingGeneFeatures.gff" inside the finalOutputDir.



## What's next?

Because of Makers' compatibility with GMOD standards, an annotation augmented in one or both of this way can be loaded into e.g. WebApollo and will save annotators a lot of work when e.g. adding meta data to transcript models.



# Submission to public repository

Once your are satisfied by the wonderful annotation yo have done, 
