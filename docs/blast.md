# Command-line Blast

## Installing blast

While you should have installed blast during the [installing software](software) tutorial, you can copy/paste the code block below to reinstall it if needed

```bash
sudo apt install ncbi-blast+
```

## Getting data

We will download some cows and human proteins from RefSeq

```bash
wget ftp://ftp.ncbi.nih.gov/refseq/B_taurus/mRNA_Prot/cow.1.protein.faa.gz
wget ftp://ftp.ncbi.nih.gov/refseq/H_sapiens/mRNA_Prot/human.1.protein.faa.gz
```

Both these files are compressed. Theu are not `tar` archives, like we encountered earlier, but `gzip` files.
To uncompress:

```bash
gzip -d *.gz
```

Let us take a look at the human file

```bash
head human.1.protein.faa
```

Both files contain protein sequences in the [FASTA format](https://en.wikipedia.org/wiki/FASTA_format)

!!! question
    How many sequences do I have in each file?

## Blast
